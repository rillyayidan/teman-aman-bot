# bot/filters/content_filter.py

BLOCKED_KEYWORDS = [
    "investasi", "keuangan", "uang", "finansial", "trading", "saham", "crypto", "bitcoin",
    "diet", "berat badan", "kesehatan umum", "tinggi badan", "olahraga",
    "pacaran", "asmara", "hubungan", "cinta", "jodoh",
    "kuliah", "kampus", "universitas", "pekerjaan", "kerja", "penghasilan"
]

def is_blocked_topic(message: str) -> bool:
    """
    Cek apakah pesan user mengandung topik yang diblokir.

    Args:
        message (str): Pesan user.

    Returns:
        bool: True jika topik terlarang terdeteksi.
    """
    message_lower = message.lower()
    return any(keyword in message_lower for keyword in BLOCKED_KEYWORDS)
