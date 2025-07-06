# database/init_db.py

import logging
from config.settings import engine
from database.models import Base

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_tables():
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Semua tabel berhasil dibuat.")
    except Exception as e:
        logger.exception(f"❌ Gagal membuat tabel: {e}")

if __name__ == "__main__":
    create_tables()
