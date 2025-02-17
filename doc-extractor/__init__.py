# doc-extractor/__init__.py

from .docExtract import PDFProcessor, PDFStructure
from .constants import (
    POPPLER_PATH,
    TESSERACT_CMD,
    SK_PATTERN,
    TITLE_PATTERN,
    MENIMBANG_PATTERN,
    BAB_PATTERN,
    PASAL_PATTERN,
    AYAT_PATTERN,
    CLOSING_PATTERN,
    LEGITIMATION_PATTERN,
    MENGINGAT_PATTERN,
)

__all__ = [
    "PDFProcessor",
    "PDFStructure",
    "POPPLER_PATH",
    "TESSERACT_CMD",
    "SK_PATTERN",
    "TITLE_PATTERN",
    "MENIMBANG_PATTERN",
    "BAB_PATTERN",
    "PASAL_PATTERN",
    "AYAT_PATTERN",
    "CLOSING_PATTERN",
    "LEGITIMATION_PATTERN",
    "MENGINGAT_PATTERN",
]
