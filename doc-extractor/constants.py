import os

# Ambil path dari environment variables atau gunakan default
POPPLER_PATH = os.getenv("POPPLER_PATH", r"poppler-24.08.0\Library\bin")
TESSERACT_CMD = os.getenv("TESSERACT_CMD", r"C:\Program Files\Tesseract-OCR\tesseract.exe")

# Regex Patterns
SK_PATTERN = r'SK No\s?\d+[A-Z]?'
TITLE_PATTERN = r"PERATURAN PRESIDEN REPUBLIK INDONESIA"
MENIMBANG_PATTERN = r"bahwa"
BAB_PATTERN = r"(BAB [IVXLCDM]+\s+[A-Z ]+)\n"
PASAL_PATTERN = r"\n(Pasal \d+)\n"
AYAT_PATTERN = r"\(\s*\d+\s*\)"
CLOSING_PATTERN = r"KETENTUAN PENUTUP"
LEGITIMATION_PATTERN = r"Ditetapkan di"
MENGINGAT_PATTERN = r"Mengingat\s*:(.*?)(?=Menetapkan|MEMUTUSKAN|$)"
