# bot/handlers/quiz_handler.py

import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from sqlalchemy.orm import Session
from config.settings import SessionLocal
from database.models import QuizQuestion, DifficultyLevel, QuestionType
from telegram.constants import ParseMode
from sqlalchemy.sql import func

logger = logging.getLogger(__name__)
user_quiz_state = {}

# === Step 1: /kuis command ===
async def kuis_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🟢 Very Easy", callback_data="quiz_start_very_easy")],
        [InlineKeyboardButton("🟡 Easy", callback_data="quiz_start_easy")],
        [InlineKeyboardButton("🟠 Medium", callback_data="quiz_start_medium")],
        [InlineKeyboardButton("🔴 Hard", callback_data="quiz_start_hard")],
        [InlineKeyboardButton("⚫ Very Hard", callback_data="quiz_start_very_hard")],
    ]
    keyboard.append([InlineKeyboardButton("🏠 Kembali ke Menu", callback_data="menu__back")])


    # Gunakan message dari callback_query jika update.message tidak tersedia
    message = update.message or update.callback_query.message
    await message.reply_text("🎯 Pilih tingkat kesulitan kuis:", reply_markup=InlineKeyboardMarkup(keyboard))

# === Step 2: Handle Level Selection & Fetch Questions ===
async def handle_quiz_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    telegram_id = query.from_user.id
    level_str = query.data.replace("quiz_start_", "")

    try:
        difficulty = DifficultyLevel[level_str]
    except KeyError:
        await query.edit_message_text("❌ Tingkat kesulitan tidak valid.")
        return

    session: Session = SessionLocal()
    try:
        questions = (
            session.query(QuizQuestion)
            .filter_by(difficulty_level=difficulty, is_active=True)
            .order_by(func.rand())
            .limit(5)
            .all()
        )
        if not questions:
            await query.edit_message_text("⚠️ Tidak ada soal untuk level ini.")
            return

        user_quiz_state[telegram_id] = {
            "questions": questions,
            "current_index": 0,
            "answers": []
        }
        context.user_data["active_feature"] = "quiz"
        await send_quiz_question(context, telegram_id)
    finally:
        session.close()


# === Helper: Send Question Based on Type ===
async def send_quiz_question(context: ContextTypes.DEFAULT_TYPE, telegram_id: int):
    state = user_quiz_state.get(telegram_id)
    if not state:
        return

    idx = state["current_index"]
    question = state["questions"][idx]

    # Build options
    if question.question_type == QuestionType.true_false:
        options = ["true", "false"]
    else:
        options = question.options  # Already a list from JSON

    keyboard = [
        [InlineKeyboardButton(opt, callback_data=f"quiz_answer_{idx}_{opt}")]
        for opt in options
    ]
    text = f"*Soal {idx+1} dari {len(state['questions'])}*\n\n{question.question}"
    keyboard.append([InlineKeyboardButton("🏠 Kembali ke Menu", callback_data="menu__back")])
    await context.bot.send_message(
        chat_id=telegram_id,
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )


# === Step 3: Handle Answer Callback ===
async def handle_quiz_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    telegram_id = query.from_user.id

    try:
        parts = query.data.split("_")
        if len(parts) < 4 or parts[0] != "quiz" or parts[1] != "answer":
            await query.edit_message_text("❌ Format jawaban tidak valid.")
            return

        idx_str = parts[2]
        selected = "_".join(parts[3:])
        idx = int(idx_str)
    except Exception as e:
        logger.exception("Error parsing answer callback")
        await query.edit_message_text("❌ Terjadi kesalahan saat memproses jawaban.")
        return

    state = user_quiz_state.get(telegram_id)
    if not state or idx != state["current_index"]:
        await query.edit_message_text("⚠️ Sesi kuis tidak valid atau sudah berubah.")
        return

    question = state["questions"][idx]
    state["answers"].append({
        "question": question.question,
        "user_answer": selected,
        "correct_answer": question.correct_answer,
        "explanation": question.explanation
    })
    state["current_index"] += 1

    if state["current_index"] >= len(state["questions"]):
        await show_quiz_results(context, telegram_id, state["answers"])
        user_quiz_state.pop(telegram_id, None)
    else:
        await send_quiz_question(context, telegram_id)


# === Step 4: Show Result ===
async def show_quiz_results(context: ContextTypes.DEFAULT_TYPE, telegram_id: int, answers: list):
    correct = sum(1 for a in answers if a["user_answer"].lower() == a["correct_answer"].lower())
    total = len(answers)

    result = f"📊 *Skor Kamu: {correct} / {total}*\n\n"
    explanations = []
    for i, a in enumerate(answers, 1):
        if a["user_answer"].lower() != a["correct_answer"].lower():
            explanations.append(
                f"*Soal {i}:*\n❓ {a['question']}\n❌ Jawabanmu: {a['user_answer']}\n✅ Benar: {a['correct_answer']}\n📝 {a['explanation']}\n"
            )

    result += "\n".join(explanations) if explanations else "🎉 Semua jawaban kamu benar. Hebat!"

    keyboard = [
        [InlineKeyboardButton("🔁 Ulangi Kuis", callback_data="quiz_restart")],
        [InlineKeyboardButton("🏠 Kembali ke Menu", callback_data="menu__back")]
    ]
    await context.bot.send_message(
        chat_id=telegram_id,
        text=result,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )

async def handle_quiz_navigation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    message = query.message

    if query.data == "quiz_restart":
        await message.reply_text("🔁 Mengulang kuis...")
        await kuis_command(update, context)