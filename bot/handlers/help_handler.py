import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from config.settings import SessionLocal
from database.models import HelpDirectory

logger = logging.getLogger(__name__)

async def bantuan_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session = SessionLocal()
    try:
        help_list = session.query(HelpDirectory).filter_by(is_active=True).order_by(HelpDirectory.order_index).all()
        if not help_list:
            await update.callback_query.message.reply_text("⚠️ Belum ada kontak bantuan yang tersedia.")
            return

        text = "📞 *Daftar Kontak Bantuan:*\n\n"
        for item in help_list:
            text += f"• *{item.name}*\n"
            if item.phone:
                text += f"  📞 Telp: {item.phone}\n"
            if item.whatsapp:
                text += f"  💬 WA: {item.whatsapp}\n"
            if item.website:
                text += f"  🌐 Web: {item.website}\n"
            if item.description:
                text += f"  📝 {item.description}\n"
            text += "\n"

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🏠 Kembali ke Menu", callback_data="menu__back")]
        ])
        await update.callback_query.message.reply_text(text, reply_markup=keyboard, parse_mode="Markdown")
    except Exception as e:
        logger.exception("Gagal mengambil data bantuan.")
        await update.callback_query.message.reply_text("❌ Terjadi kesalahan saat mengambil data bantuan.")
    finally:
        session.close()
