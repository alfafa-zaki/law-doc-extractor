# Law PDF Document Extractor

A Python library to process and extract structured data from Law PDF Documents (Peraturan Presiden Republik Indonesia). This library is designed to extract text, identify sections, and structure (BAB, Ayat, Pasal) the content of law PDF documents, especially legal or regulatory documents.

## Installation

Install the library:

```bash
pip install git+https://github.com/alfafa-zaki/law-doc-extractor.git
```

## Prerequisites
Before using this library, install Poppler and Tesseract on your system.
1. Install Poppler (required to convert PDF pages to images)
   #### On Ubuntu/Debian:
   ```bash
   sudo apt-get install poppler-utils
   ```
   #### On macOS:
   ```bash
   brew install poppler
   ```
   #### On Windows
   - Download Poppler from this link: https://github.com/oschwartz10612/poppler-windows
   - Extract the zip file and note the path to the bin folder (e.g., C:\path\to\poppler\bin).

2. Install Tesseract (required for OCR - Optical Character Recognition)
   
