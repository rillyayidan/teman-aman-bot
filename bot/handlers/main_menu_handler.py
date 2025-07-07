# bot/handlers/main_menu_handler.py

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from bot.state.session_manager import set_user_session, clear_user_session

logger = logging.getLogger(__name__)

# Fungsi utama: /menu command
async def main_menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await clear_user_session(user_id)  # Reset sesi aktif

    keyboard = [
        [
            InlineKeyboardButton("💬 AI Chat", callback_data="menu__ai_chat"),
            InlineKeyboardButton("📚 Edukasi", callback_data="menu__edukasi")
        ],
        [
            InlineKeyboardButton("📝 Kuis", callback_data="menu__kuis"),
            InlineKeyboardButton("🆘 Bantuan", callback_data="menu__bantuan")
        ],
        [
            InlineKeyboardButton("🔐 Privasi", callback_data="menu__privasi")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Gunakan message atau callback.message
    if update.message:
        await update.message.reply_text(
            "🏠 *Menu Utama*\nSilakan pilih fitur yang ingin kamu gunakan:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    elif update.callback_query:
        await update.callback_query.edit_message_text(
            "🏠 *Menu Utama*\nSilakan pilih fitur yang ingin kamu gunakan:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )


# Fungsi callback ketika tombol fitur diklik
async def menu_router_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    data = query.data  # Contoh: "menu__edukasi"
    feature = data.split("__")[1]
    if feature == "back":
        await main_menu_command(update, context)
        return

    await clear_user_session(user_id)
    await set_user_session(user_id, feature)

    if feature == "ai_chat":
        await query.message.reply_text("💬 *AI Chat aktif*. Ketik pertanyaanmu kapan saja.", parse_mode="Markdown")

    elif feature == "edukasi":
        from .education_handler import edukasi_command
        # Simulasikan perintah edukasi
        fake_update = Update(update.update_id, message=query.message)  # agar edukasi_command bisa jalan
        await edukasi_command(fake_update, context)

    elif feature == "kuis":
        from .quiz_handler import kuis_command
        fake_update = Update(update.update_id, message=query.message)
        await kuis_command(fake_update, context)

    elif feature == "bantuan":
        from .help_handler import bantuan_command
        await bantuan_command(update, context)


    elif feature == "privasi":
        from .privacy_handler import privasi_command
        await privasi_command(update, context)

    else:
        await query.message.reply_text("❌ Fitur tidak dikenali.")
