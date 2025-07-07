import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    CommandHandler,
    filters,
    CallbackQueryHandler
)
from bot.handlers.ai_chat_handler import ai_chat_handler
from bot.handlers.education_handler import (
    edukasi_command,
    kategori_dipilih_callback,
    konten_dipilih_callback
)
from bot.handlers.quiz_handler import (
    kuis_command,
    handle_quiz_start,
    handle_quiz_answer,
    handle_quiz_navigation  # ⬅️ Tambahan ini diperlukan
)
from bot.handlers.main_menu_handler import main_menu_command, menu_router_callback
from bot.handlers.help_handler import bantuan_command
from bot.handlers.privacy_handler import privasi_command

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ===============================
# /start Command Handler
# ===============================
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "👋 Halo, aku *Teman Aman*, asisten AI untuk edukasi kekerasan seksual.\n\n"
        "🛡️ Aku dirancang untuk membantu kamu memahami topik seperti *consent*, mengenali tanda-tanda kekerasan, "
        "dan cara mencari bantuan.\n\n"
        "📚 Gunakan menu untuk memilih: Edukasi, Kuis, Bantuan, atau Chat AI.\n\n"
        "Ketik /menu untuk melihat fitur yang ingin digunakan"
    )
    await update.message.reply_text(welcome_text, parse_mode=ParseMode.MARKDOWN)

# ===============================
# Fallback handler (tidak dikenali)
# ===============================
async def unknown_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❓ Maaf, saya tidak memahami pesan itu. Coba ketik sesuatu yang lain.")

# ===============================
# Main Bot Setup
# ===============================
def main():
    if not BOT_TOKEN:
        logger.error("❌ BOT_TOKEN tidak ditemukan di .env")
        return

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Command: /start
    app.add_handler(CommandHandler("start", start_command))

    # AI Chat Handler: semua pesan teks biasa
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_chat_handler))

    # Education Handler
    app.add_handler(CommandHandler("edukasi", edukasi_command))
    app.add_handler(CallbackQueryHandler(kategori_dipilih_callback, pattern=r"^edu_cat_\d+$"))
    app.add_handler(CallbackQueryHandler(konten_dipilih_callback, pattern=r"^edu_content_\d+$"))

    # Quiz Handler
    app.add_handler(CommandHandler("kuis", kuis_command))
    app.add_handler(CallbackQueryHandler(handle_quiz_start, pattern=r"^quiz_start_"))
    app.add_handler(CallbackQueryHandler(handle_quiz_answer, pattern=r"^quiz_answer_"))
    app.add_handler(CallbackQueryHandler(handle_quiz_navigation, pattern=r"^quiz_restart$"))

    # Main Menu
    app.add_handler(CommandHandler("menu", main_menu_command))
    app.add_handler(CallbackQueryHandler(menu_router_callback, pattern="^menu__"))

    # Bantuan
    app.add_handler(CommandHandler("bantuan", bantuan_command))

    # Privacy
    app.add_handler(CommandHandler("privasi", privasi_command))
    # Fallback handler untuk pesan yang tidak diproses
    app.add_handler(MessageHandler(filters.ALL, unknown_message))

    # Jalankan Bot
    logger.info("🤖 Bot Teman Aman sedang berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
