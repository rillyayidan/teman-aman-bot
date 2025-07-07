# bot/handlers/main_menu_handler.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from bot.state.session_manager import clear_user_feature
from bot.state.session_manager import set_user_feature
from bot.handlers.education_handler import edukasi_command
from bot.handlers.quiz_handler import kuis_command

async def main_menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    clear_user_feature(telegram_id)

    keyboard = [
        [InlineKeyboardButton("📚 Edukasi", callback_data="menu_edukasi")],
        [InlineKeyboardButton("🧠 Kuis", callback_data="menu_kuis")],
        [InlineKeyboardButton("🤖 Chat AI", callback_data="menu_aichat")],
        [InlineKeyboardButton("🆘 Bantuan", callback_data="menu_bantuan")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🏠 *Menu Utama*\nSilakan pilih fitur:", reply_markup=reply_markup, parse_mode="Markdown")
    
async def menu_router_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    telegram_id = query.from_user.id

    if query.data == "menu_edukasi":
        set_user_feature(telegram_id, "edukasi")
        await edukasi_command(update, context)

    elif query.data == "menu_kuis":
        set_user_feature(telegram_id, "kuis")
        await kuis_command(update, context)

    elif query.data == "menu_aichat":
        set_user_feature(telegram_id, "ai_chat")
        await query.edit_message_text("💬 Silakan ketik pertanyaanmu. Aku akan menjawab sebagai AI Chat.")
    
    elif query.data == "menu_bantuan":
        set_user_feature(telegram_id, "bantuan")
        await query.edit_message_text("📞 Untuk bantuan, hubungi layanan resmi di ...")