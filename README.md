TemanAman
---

````markdown
# 🤖 Teman Aman Bot

Teman Aman adalah ChatBot Telegram berbasis AI yang dirancang untuk membantu anak muda memahami isu kekerasan seksual secara aman, edukatif, dan interaktif.  
Bot ini menyediakan fitur **AI Chat**, **Edukasi Tematik**, **Kuis Pemahaman**, dan informasi **Bantuan Darurat** & **Privasi Pengguna**.

---

## 🚀 Fitur Utama

| Fitur        | Deskripsi                                                                 |
|--------------|---------------------------------------------------------------------------|
| 💬 **AI Chat**      | Chat interaktif berbasis GPT-4o yang menjaga keamanan & konteks user.   |
| 📚 **Edukasi**      | Materi edukasi bertema kekerasan seksual berdasarkan kategori.         |
| 📝 **Kuis**         | Latihan soal dengan 5 pertanyaan acak sesuai tingkat kesulitan.        |
| 🆘 **Bantuan**      | Daftar kontak lembaga bantuan darurat, hotline, dan website resmi.     |
| 🔐 **Privasi**      | Informasi kebijakan privasi Teman Aman dan cara perlindungan data.     |

---

## 🛠️ Tech Stack

- **Python 3.11+**
- **[python-telegram-bot](https://docs.python-telegram-bot.org/en/stable/)** `v20.7`
- **OpenAI API (GPT-4o)**
- **MySQL** (via `SQLAlchemy ORM`)
- **FastAPI (Opsional untuk ekstensi API ke depan)**
- **Laragon + phpMyAdmin** untuk pengelolaan database lokal

---

## 📦 Instalasi & Setup

### 1. Clone Repository

```bash
git clone https://github.com/kamu/teman-aman-bot.git
cd teman-aman-bot
````

### 2. Install Dependency

```bash
pip install -r requirements.txt
```

### 3. Konfigurasi `.env`

Buat file `.env` di root folder:

```
BOT_TOKEN=your-telegram-bot-token
OPENAI_API_KEY=your-openai-api-key
DB_HOST=localhost
DB_PORT=3306
DB_NAME=teman_aman_bot
DB_USER=root
DB_PASSWORD=
```

### 4. Inisialisasi Database

```bash
python -m database.init_db
```

Tambahkan data dummy melalui phpMyAdmin untuk tabel:

* `content_categories`
* `educational_content`
* `quiz_questions`
* `help_directory`
* `privacy_content`

### 5. Jalankan Bot

```bash
python -m bot.main
```

---

## 🧠 Struktur Proyek

```
teman-aman-bot/
├── bot/
│   ├── handlers/               # Semua fitur/fitur handler Telegram
│   │   ├── ai_chat_handler.py
│   │   ├── education_handler.py
│   │   ├── quiz_handler.py
│   │   ├── help_handler.py
│   │   ├── privacy_handler.py
│   │   └── main_menu_handler.py
│   └── state/
│       └── session_manager.py  # Manajemen sesi pengguna aktif
├── database/
│   ├── models.py               # Definisi semua tabel
│   └── init_db.py              # Setup awal database
├── config/
│   └── settings.py             # Konfigurasi DB & API Key
├── requirements.txt
└── main.py                     # Entry point utama bot
```

---

## 🧪 Panduan Testing Lokal

* Jalankan bot di terminal dan buka Telegram.
* Gunakan `/menu` untuk membuka fitur utama.
* Tes tiap fitur secara berurutan (AI Chat, Edukasi, Kuis, Bantuan, Privasi).
* Jika perlu debug, lihat `logging` di terminal.

---

## 🔒 Catatan Privasi

Teman Aman menyimpan:

* Pesan dan jawaban AI untuk evaluasi keamanan.
* ID Telegram untuk sesi dan pelacakan interaksi.
* Tidak menyimpan data sensitif atau identitas pengguna tanpa izin.

---

## 👥 Kontribusi

Pull Request dan issue sangat terbuka — terutama untuk:

* Penambahan konten edukasi
* Soal kuis baru
* Integrasi layanan darurat lokal

---

## 🧾 Lisensi

MIT License © 2025 - Tim Teman Aman
Tidak untuk penggunaan komersial tanpa izin.

---
