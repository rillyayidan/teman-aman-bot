# bot/handlers/ai_chat_handler.py

import logging
from openai import OpenAI
from telegram import Update
from telegram.ext import ContextTypes
from config.settings import OPENAI_API_KEY, SessionLocal
from bot.prompts.openai_prompt import SYSTEM_PROMPT
from database.models import User, ConversationLog, MessageType
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from bot.filters.content_filter import is_blocked_topic

# Setup OpenAI Client
client = OpenAI(api_key=OPENAI_API_KEY)

# Setup logger
logger = logging.getLogger(__name__)

async def ai_chat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.strip()
    telegram_user = update.effective_user
    
    if is_blocked_topic(user_message):
        await update.message.reply_text(
            "⚠️ Maaf, aku hanya bisa bantu untuk topik kekerasan seksual, consent, pelecehan, bullying, dan perlindungan diri. "
            "Untuk pertanyaan seperti itu, silakan cari bantuan dari sumber yang lebih tepat ya. 🙏"
        )
        return
    
    if not user_message:
        await update.message.reply_text("❗ Mohon ketik sesuatu.")
        return

    session = SessionLocal()
    try:
        # 1. Ambil / buat user
        user = session.query(User).filter_by(telegram_id=telegram_user.id).first()
        if not user:
            user = User(telegram_id=telegram_user.id)
            session.add(user)
            session.commit()
            session.refresh(user)
        else:
            user.total_interactions += 1
        user.last_activity = func.now()
        session.commit()

        # 2. Ambil histori chat terakhir user (misalnya 5 pesan terakhir)
        previous_logs = (
            session.query(ConversationLog)
            .filter_by(user_id=user.id)
            .order_by(ConversationLog.timestamp.desc())
            .limit(5)
            .all()
        )
        # Susun ke format messages OpenAI
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for log in reversed(previous_logs):
            messages.append({"role": "user", "content": log.user_message})
            if log.ai_response:
                messages.append({"role": "assistant", "content": log.ai_response})
        # Tambahkan pesan terbaru dari user
        messages.append({"role": "user", "content": user_message})

        # 3. Kirim ke OpenAI
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.3,
            max_tokens=500
        )
        ai_reply = response.choices[0].message.content
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🏠 Kembali ke Menu", callback_data="menu__back")]
        ])
        await update.message.reply_text(ai_reply, reply_markup=keyboard)


        # 4. Simpan log chat
        log = ConversationLog(
            user_id=user.id,
            message_type=MessageType.crisis_detection,
            user_message=user_message,
            ai_response=ai_reply,
            is_resolved=False
        )
        session.add(log)
        session.commit()

    except SQLAlchemyError as db_err:
        logger.exception(f"❌ DB Error: {db_err}")
        await update.message.reply_text("⚠️ Maaf, terjadi kesalahan pada database. Coba lagi nanti.")

    except Exception as e:
        logger.exception(f"❌ Error saat memproses permintaan AI: {e}")
        await update.message.reply_text("⚠️ Maaf, terjadi kesalahan saat menghubungi AI. Silakan coba lagi nanti.")

    finally:
        session.close()
