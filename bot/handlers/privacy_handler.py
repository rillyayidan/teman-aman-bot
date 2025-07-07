import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from config.settings import SessionLocal
from database.models import PrivacyContent

logger = logging.getLogger(__name__)

async def privasi_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session = SessionLocal()
    try:
        entry = session.query(PrivacyContent).filter_by(is_active=True).order_by(PrivacyContent.order_index).first()
        if not entry:
            await update.callback_query.message.reply_text("⚠️ Informasi privasi belum tersedia.")
            return

        text = f"🔐 *{entry.title}*\n\n{entry.content}"
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🏠 Kembali ke Menu", callback_data="menu__back")]
        ])
        await update.callback_query.message.reply_text(text, reply_markup=keyboard, parse_mode="Markdown")
    except Exception as e:
        logger.exception("Gagal mengambil data privasi.")
        await update.callback_query.message.reply_text("❌ Terjadi kesalahan saat mengambil informasi privasi.")
    finally:
        session.close()
