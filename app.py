import gradio as gr
import os
import nltk
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from fpdf import FPDF
from gtts import gTTS
from pdfminer.high_level import extract_text
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

nltk.download('punkt')

# Load the models and tokenizers
tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")

# Convert DOCX to PDF using reportlab
def docx_to_pdf(docx_file, output_pdf="converted_doc.pdf"):
    doc = Document(docx_file)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    
    pdf = canvas.Canvas(output_pdf, pagesize=letter)
    pdf.setFont("Helvetica", 12)
    
    text = pdf.beginText(40, 750)
    for line in full_text:
        text.textLine(line)
    
    pdf.drawText(text)
    pdf.save()
    return output_pdf

# Process input file (PDF or DOCX)
def pdf_to_text(text, PDF, min_length=20):
    try:
        file_extension = os.path.splitext(PDF.name)[1].lower()
        
        if file_extension == '.docx':
            pdf_file_path = docx_to_pdf(PDF.name)
            text = extract_text(pdf_file_path)
        elif file_extension == '.pdf' and text == "":
            text = extract_text(PDF.name)
        
        inputs = tokenizer([text], max_length=1024, truncation=True, return_tensors="pt")
        min_length = int(min_length)
        
        summary_ids = model.generate(inputs["input_ids"], num_beams=2, min_length=min_length, max_length=min_length+1000)
        output_text = tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Times", size=12)
        pdf.multi_cell(190, 10, txt=output_text, align='C')
        pdf_output_path = "legal.pdf"
        pdf.output(pdf_output_path)
        
        audio_output_path = "legal.wav"
        tts = gTTS(text=output_text, lang='en', slow=False)
        tts.save(audio_output_path)
        
        return audio_output_path, output_text, pdf_output_path
    
    except Exception as e:
        return None, f"An error occurred: {str(e)}", None

# Preloaded document handler
def process_sample_document(min_length=20):
    sample_document_path = "Marbury v. Madison.pdf"
    
    with open(sample_document_path, "rb") as f:
        return pdf_to_text("", f, min_length)

# Gradio interface
with gr.Blocks() as iface:
    with gr.Row():
        process_sample_button = gr.Button("Summarize Marbury v. Madison Case Pre-Uploaded")
    
    text_input = gr.Textbox(label="Input Text")
    file_input = gr.File(label="Upload PDF or DOCX")
    slider = gr.Slider(minimum=10, maximum=100, step=10, value=20, label="Summary Minimum Length")
    
    audio_output = gr.Audio(label="Generated Audio")
    summary_output = gr.Textbox(label="Generated Summary")
    pdf_output = gr.File(label="Summary PDF")
    
    process_sample_button.click(fn=process_sample_document, inputs=slider, outputs=[audio_output, summary_output, pdf_output])
    file_input.change(fn=pdf_to_text, inputs=[text_input, file_input, slider], outputs=[audio_output, summary_output, pdf_output])

if __name__ == "__main__":
    iface.launch()
