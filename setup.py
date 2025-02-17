from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="LawDocExtractor",
    version="0.1.0",
    author="Alfafa Zaki",
    author_email="alfafa26zaki@gmail.com",
    description="A library to process and extract structured data from law (Peraturan Presiden) PDF document.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alfafa-zaki/law-doc-extractor",
    packages=find_packages(include=["LawDocExtractor", "LawDocExtractor.*"]),
    install_requires=[
        "pypdf>=3.0.0",
        "pytesseract>=0.3.10",
        "pdf2image>=1.16.3",
        "pydantic>=2.0.0",
        "Pillow>=10.0.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
