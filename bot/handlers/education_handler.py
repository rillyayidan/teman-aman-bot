from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, CallbackQueryHandler, CommandHandler
from database.models import ContentCategory, EducationalContent
from config.settings import SessionLocal
import logging

logger = logging.getLogger(__name__)

# Command: /edukasi
async def edukasi_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session = SessionLocal()
    try:
        categories = session.query(ContentCategory).filter_by(is_active=True).order_by(ContentCategory.order_index).all()
        if not categories:
            await update.message.reply_text("⚠️ Belum ada kategori edukasi yang tersedia.")
            return

        keyboard = [
            [InlineKeyboardButton(cat.name, callback_data=f"edu_cat_{cat.id}")]
            for cat in categories
        ]
        keyboard.append([InlineKeyboardButton("🏠 Kembali ke Menu", callback_data="menu__back")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("📚 Pilih kategori edukasi:", reply_markup=reply_markup)
    except Exception as e:
        logger.exception(f"Error saat mengambil kategori edukasi: {e}")
        await update.message.reply_text("❌ Terjadi kesalahan saat mengambil data edukasi.")
    finally:
        session.close()

async def kategori_dipilih_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    category_id = query.data.replace("edu_cat_", "")
    session = SessionLocal()
    try:
        contents = session.query(EducationalContent).filter_by(
            category_id=category_id, is_active=True
        ).order_by(EducationalContent.order_index).all()

        if not contents:
            await query.edit_message_text("⚠️ Konten untuk kategori ini belum tersedia.")
            return

        keyboard = [
            [InlineKeyboardButton(content.title, callback_data=f"edu_content_{content.id}")]
            for content in contents
        ]
        keyboard.append([InlineKeyboardButton("🏠 Kembali ke Menu", callback_data="menu__back")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("📄 Pilih konten untuk dibaca:", reply_markup=reply_markup)
    except Exception as e:
        logger.exception(f"Error saat mengambil konten edukasi: {e}")
        await query.edit_message_text("❌ Terjadi kesalahan saat mengambil konten.")
    finally:
        session.close()
        
async def konten_dipilih_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    content_id = query.data.replace("edu_content_", "")
    session = SessionLocal()
    try:
        content = session.query(EducationalContent).filter_by(id=content_id, is_active=True).first()
        if not content:
            await query.edit_message_text("⚠️ Konten tidak ditemukan.")
            return

        text = f"📘 *{content.title}*\n\n{content.content}"
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🏠 Kembali ke Menu", callback_data="menu__back")]
        ])
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=keyboard)
    except Exception as e:
        logger.exception(f"Error saat menampilkan konten edukasi: {e}")
        await query.edit_message_text("❌ Terjadi kesalahan saat menampilkan konten.")
    finally:
        session.close()
