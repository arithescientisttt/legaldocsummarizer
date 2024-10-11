Lincoln Legal AI: Automated Legal Document Summarization & Audio Generation Tool
================================================================================

Welcome to the **Lincoln Legal AI** project! This tool leverages cutting-edge natural language processing (NLP) models to provide automatic summarization and audio narration of legal documents. Whether you're a legal professional, student, or someone interested in law, our tool simplifies the process of understanding complex legal texts.

Features
--------

*   Summarize legal documents (PDF or DOCX) using advanced AI models.
*   Generate audio versions of summaries using high-quality text-to-speech (TTS).
*   Download summaries in both text and PDF formats.
*   Intuitive web-based interface with easy upload functionality.

Usage Instructions
------------------

To use this tool, follow these steps:

1.  Clone this repository to your local machine:

    git clone https://github.com/arithescientisttt/legaldocsummarize.git

3.  Install the required dependencies:

    pip install -r requirements.txt

5.  Run the application locally:

    python app.py

7.  Open your browser and go to [http://localhost:7860](http://localhost:7860) to access the interface.

Live Demo
---------

Try out the live version of Lincoln Legal AI directly via: [arithescientist.com/lincolnlegal](http://arithescientist.com/lincolnlegal).

Technologies Used
-----------------

*   [Hugging Face Transformers](https://huggingface.co/) for summarization using BART model.
*   [PDFMiner](https://pypi.org/project/pdfminer.six/) for PDF text extraction.
*   [python-docx](https://pypi.org/project/docx/) for DOCX file handling.
*   [gTTS](https://pypi.org/project/gTTS/) for text-to-speech conversion.
*   [Gradio](https://gradio.app/) for building the user interface.
*   [FPDF](https://pypi.org/project/fpdf/) for generating PDF summaries.
