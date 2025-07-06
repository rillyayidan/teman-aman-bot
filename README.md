# 🤖 Teman Aman Bot

Telegram bot edukasi kekerasan seksual dengan fitur privasi tinggi dan integrasi AI.

## 🚀 Fitur Utama
- Chat AI seputar kekerasan seksual (berbasis GPT)
- Sistem edukasi dinamis
- Kuis kesadaran
- Direktori bantuan (darurat, hukum, konseling)
- Fitur privasi dan panic button

## 🛠️ Cara Menjalankan

```bash
# 1. Clone repository
git clone https://github.com/your-org/teman-aman-bot.git
cd teman-aman-bot

# 2. Setup virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Siapkan file .env
cp .env.example .env

# 5. Jalankan test koneksi
python database/test_connection.py

# 6. Jalankan bot
python bot/main.py
