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
)
from bot.handlers.ai_chat_handler import ai_chat_handler

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
        "Ketik *apapun* untuk memulai percakapan atau gunakan tombol menu yang tersedia."
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

    # Fallback handler untuk pesan yang tidak diproses
    app.add_handler(MessageHandler(filters.ALL, unknown_message))

    # Jalankan Bot
    logger.info("🤖 Bot Teman Aman sedang berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
