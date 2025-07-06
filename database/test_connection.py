from config.settings import engine
from sqlalchemy import text

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("✅ MySQL connection successful:", result.scalar())
except Exception as e:
    print("❌ Connection failed:", str(e))
