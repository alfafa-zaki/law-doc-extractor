# Law PDF Document Extractor

A Python library to process and extract structured data from Law PDF Documents (Peraturan Presiden Republik Indonesia). This library is designed to extract text, identify sections, and structure (BAB, Ayat, Pasal) the content of law PDF documents, especially legal or regulatory documents.

## Installation
Install Packages:
```bash
pip install -r requirements.txt
```
Install library:
```bash
pip install git+https://github.com/alfafa-zaki/law-doc-extractor.git
```

## Prerequisites
Before using this library, install Poppler and Tesseract on your system.
1. Install Poppler (required to convert PDF pages to images)
   ##### On Ubuntu/Debian:
   ```bash
   sudo apt-get install poppler-utils
   ```
   On macOS:
   ```bash
   brew install poppler
   ```
   On Windows
   - Download Poppler from this link: https://github.com/oschwartz10612/poppler-windows
   - Extract the zip file and note the path to the bin folder (e.g., C:\path\to\poppler\bin).

3. Install Tesseract (required for OCR - Optical Character Recognition)
   On Ubuntu/Debian:
   ```bash
   sudo apt-get install tesseract-ocr
   ```
   On macOS:
   ```bash
   brew install tesseract
   ```
   On Windows
   - Download the Tesseract installer from this link: https://github.com/UB-Mannheim/tesseract/wiki
   - Run the installer and note the installation path (e.g., C:\Program Files\Tesseract-OCR).

## Usage
### Step 1: Set Environment Variables
Set the paths to Poppler and Tesseract in environment variables.
On Ubuntu/macOS:
Add the following lines to .bashrc, .zshrc, or .bash_profile:
```bash
export POPPLER_PATH="/path/to/poppler/bin"
export TESSERACT_CMD="/path/to/tesseract"
```
On Windows
Open Command Prompt and run:
```cmd
set POPPLER_PATH=C:\path\to\poppler\bin
set TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
```
Alternatively, create a config.json file in the root directory:
```json
{
  "POPPLER_PATH": "/path/to/poppler/bin",
  "TESSERACT_CMD": "/path/to/tesseract"
}
```
### Step 2: Use the Library
```python
from LawDocExtractor import PDFProcessor
import json

# Path to your PDF file
pdf_path = "path/to/your/pdf.pdf"

# Initialize the processor
processor = PDFProcessor(pdf_path)

# Process the PDF (True: Include Ayat | False: Exclude Ayat)
final_structure = processor.process(include_ayat=False)

# Print the result
print(json.dumps(final_structure.model_dump(), indent=2, ensure_ascii=False))
```

## Output Example
```json
{
  "JUDUL": "PERATURAN PRESIDEN REPUBLIK INDONESIA...",
  "MENIMBANG": "bahwa dalam rangka...",
  "MENGINGAT": "Undang-Undang Nomor 12 Tahun 2024...",
  "BATANG_TUBUH": {
    "BAB I KETENTUAN UMUM": {
      "Pasal 1": "Dalam Peraturan Presiden ini yang dimaksud dengan..."
    }
  },
  "PENUTUP": "Peraturan Presiden ini mulai berlaku pada tanggal...",
  "PENGESAHAN": "Ditetapkan di Jakarta pada tanggal..."
}
```
