import re
import os
import json
import logging
import pytesseract
from PIL import Image
from pypdf import PdfReader
from pydantic import BaseModel
from pdf2image import convert_from_path
from typing import Dict, List, Optional, Union

# Constants
POPPLER_PATH = r"D:\2025\RAG\poppler-24.08.0\Library\bin"
TESSERACT_CMD = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
SK_PATTERN = r'SK No\s?\d+[A-Z]?'
TITLE_PATTERN = r"PERATURAN PRESIDEN REPUBLIK INDONESIA"
MENIMBANG_PATTERN = r"bahwa"
BAB_PATTERN = r"(BAB [IVXLCDM]+\s+[A-Z ]+)\n"
PASAL_PATTERN = r"\n(Pasal \d+)\n"
AYAT_PATTERN = r"\(\s*\d+\s*\)"
CLOSING_PATTERN = r"KETENTUAN PENUTUP"
LEGITIMATION_PATTERN = r"Ditetapkan di"
MENGINGAT_PATTERN = r"Mengingat\s*:(.*?)(?=Menetapkan|MEMUTUSKAN|$)"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFStructure(BaseModel):
    JUDUL: str
    MENIMBANG: str
    MENGINGAT: str
    BATANG_TUBUH: Dict[str, Dict[str, Union[Dict[str, str], str]]]
    PENUTUP: str
    PENGESAHAN: str

class PDFProcessor:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path

    def extract_text_pdf(self) -> str:
        """Extract text from PDF."""
        try:
            read = PdfReader(self.pdf_path)
            pdf_text = [p.extract_text().strip() for p in read.pages if p.extract_text()]
            return "\n\n".join(pdf_text)
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {e}")
            raise

    def extract_sk_numbers(self, full_text: str) -> List[str]:
        """Extract SK numbers from text."""
        return re.findall(SK_PATTERN, full_text)

    def clean_text(self, full_text: str) -> str:
        """Clean the extracted text."""
        full_text = re.sub(r'^SALINAN\s*', '', full_text, count=1, flags=re.MULTILINE)
        full_text = re.sub(r'PRESIDEN\s*\nREPUBLIK INDONESIA', '', full_text, flags=re.MULTILINE)
        full_text = re.sub(r'-[a-zA-Z0-9\s]-', '', full_text)
        full_text = re.sub(r'\n?[a-zA-Z0-9\s]*\.\.\.?\s*', '', full_text)
        full_text = re.sub(r'\n?[a-zA-Z0-9\s]*\.\s*\.\s*', '', full_text)
        full_text = re.sub(SK_PATTERN, '', full_text)
        return full_text

    def identify_structure(self, full_text: str, include_ayat: bool = False) -> Dict:
        """Identify and structure the content of the PDF."""
        structure = {
            "JUDUL": "",
            "MENIMBANG": "",
            "BATANG_TUBUH": {},
            "PENUTUP": "",
            "PENGESAHAN": ""
        }

        if TITLE_PATTERN in full_text:
            tittle_start = full_text.find(TITLE_PATTERN)
            tittle_end = full_text.find("DENGAN RAHMAT TUHAN YANG MAHA ESA")
            structure["JUDUL"] = full_text[tittle_start:tittle_end]

        if MENIMBANG_PATTERN in full_text:
            menimbang_start = full_text.find(MENIMBANG_PATTERN)
            menimbang_end = full_text.find(";\n")
            structure["MENIMBANG"] = full_text[menimbang_start:menimbang_end]

        bab_matches = list(re.finditer(BAB_PATTERN, full_text, re.DOTALL))
        for i, match in enumerate(bab_matches):
            bab_title = match.group(1).replace("\n", " ").strip()
            start_index = match.start()
            end_index = bab_matches[i + 1].start() if i + 1 < len(bab_matches) else full_text.find(LEGITIMATION_PATTERN)
            
            if end_index == -1:
                end_index = full_text.find(LEGITIMATION_PATTERN)
            
            if end_index == -1:
                end_index = len(full_text)
            
            bab_content = full_text[start_index:end_index].strip()
            
            pasal_matches = list(re.finditer(PASAL_PATTERN, bab_content, re.DOTALL))
            
            bab_structure = {}
            for j, pasal_match in enumerate(pasal_matches):
                pasal_title = pasal_match.group(1).strip()
                pasal_start = pasal_match.start()
                pasal_end = pasal_matches[j + 1].start() if j + 1 < len(pasal_matches) else len(bab_content)
                
                pasal_content = bab_content[pasal_start:pasal_end].strip()
                pasal_content = re.sub(r"^Pasal \d+", "", pasal_content).strip()
                
                if include_ayat:
                    ayat_matches = list(re.finditer(AYAT_PATTERN, pasal_content))
                    
                    if ayat_matches:
                        ayat_structure = {}
                        for k, ayat_match in enumerate(ayat_matches):
                            ayat_start = ayat_match.start()
                            ayat_end = ayat_matches[k + 1].start() if k + 1 < len(ayat_matches) else len(pasal_content)
                            
                            ayat_number = ayat_match.group(0).strip()
                            ayat_content = pasal_content[ayat_start:ayat_end].strip()
                            ayat_content = re.sub(r"\(\s*\d+\s*\)", "", ayat_content, count=1).strip()
                            
                            ayat_structure[ayat_number] = ayat_content
                        
                        bab_structure[pasal_title] = ayat_structure
                    else:
                        bab_structure[pasal_title] = pasal_content.strip()
                else:
                    bab_structure[pasal_title] = pasal_content.strip()
            
            structure["BATANG_TUBUH"][bab_title] = bab_structure

        if CLOSING_PATTERN in full_text:
            closing_start = full_text.find(CLOSING_PATTERN)
            legitimation_start = full_text.find(LEGITIMATION_PATTERN)
            structure["PENUTUP"] = full_text[closing_start:legitimation_start]
        
        if LEGITIMATION_PATTERN in full_text:
            legitimation_start = full_text.find(LEGITIMATION_PATTERN)
            legitimation_end = full_text.find("LEMBARAN NEGARA REPUBLIK INDONESIA")
            structure["PENGESAHAN"] = full_text[legitimation_start:legitimation_end]

        return structure

    def clean_text2(self, text: str) -> str:
        """Further clean the text."""
        cleaned_text2 = re.sub(r'\n+', ' ', text)
        cleaned_text2 = re.sub(r'\s+', ' ', cleaned_text2)
        cleaned_text2 = re.sub(r'[^\x00-\x7F]+', '', cleaned_text2)
        cleaned_text2 = re.sub(r'[\x00-\x1F\x7F]', '', cleaned_text2)
        return cleaned_text2.strip()

    def clean_structure(self, structure: Dict) -> Dict:
        """Clean the structure dictionary."""
        cleaned_structure = {}
        for key, value in structure.items():
            if isinstance(value, str):
                cleaned_structure[key] = self.clean_text2(value)
            elif isinstance(value, dict):
                cleaned_structure[key] = self.clean_structure(value)
            else:
                cleaned_structure[key] = value
        return cleaned_structure

    def pdf_to_png(self) -> Optional[str]:
        """Convert the first page of the PDF to a PNG image."""
        try:
            filename = os.path.basename(self.pdf_path)
            name_without_ext = os.path.splitext(filename)[0]
            output_path = f"page1_{name_without_ext}.png"
            pages = convert_from_path(self.pdf_path, first_page=1, last_page=1, poppler_path=POPPLER_PATH)
            if pages:
                pages[0].save(output_path, "PNG")
                return output_path
            return None
        except Exception as e:
            logger.error(f"Error converting PDF to PNG: {e}")
            raise

    def load_image(self, image_path: str) -> Image:
        """Load an image from the given path."""
        try:
            return Image.open(image_path)
        except Exception as e:
            logger.error(f"Error loading image: {e}")
            raise

    def extract_image_to_text(self, image: Image) -> str:
        """Extract text from an image using OCR."""
        try:
            pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD
            return pytesseract.image_to_string(image)
        except Exception as e:
            logger.error(f"Error extracting text from image: {e}")
            raise

    def identify_sections(self, text: str) -> Dict[str, str]:
        """Identify specific sections in the text."""
        sections = {"MENGINGAT": ""}
        match = re.search(MENGINGAT_PATTERN, text, re.DOTALL)
        if match:
            extracted_text = match.group(1).strip().replace("\n", " ")
            extracted_text = re.sub(r'\s+', ' ', extracted_text)
            sections["MENGINGAT"] = extracted_text
        else:
            sections["MENGINGAT"] = "Tidak ditemukan"
        return sections

    def process(self, include_ayat: bool = False) -> PDFStructure:
        """Process the PDF and return the structured data."""
        try:
            full_text = self.extract_text_pdf()
            sk_number = self.extract_sk_numbers(full_text)
            full_text = self.clean_text(full_text)

            structure = self.identify_structure(full_text, include_ayat=include_ayat)
            cleaned_structure = self.clean_structure(structure)

            image_path = self.pdf_to_png()
            if image_path:
                image = self.load_image(image_path)
                extracted_text = self.extract_image_to_text(image)
                sections = self.identify_sections(extracted_text)

            final_structure = PDFStructure(
                JUDUL=cleaned_structure["JUDUL"],
                MENIMBANG=cleaned_structure.get("MENIMBANG", ""),
                MENGINGAT=sections.get("MENGINGAT", ""),
                BATANG_TUBUH=cleaned_structure["BATANG_TUBUH"],
                PENUTUP=cleaned_structure["PENUTUP"],
                PENGESAHAN=cleaned_structure["PENGESAHAN"]
            )

            return final_structure
        except Exception as e:
            logger.error(f"Error processing PDF: {e}")
            raise

# Example usage
if __name__ == "__main__":
    pdf_path = "documents/perpres/perpres-no-161-tahun-2024.pdf"
    processor = PDFProcessor(pdf_path)

    # Option: include_ayat=True to extract down to ayat level
    final_structure = processor.process(include_ayat=False)
    print(json.dumps(final_structure.model_dump(), indent=2, ensure_ascii=False))
