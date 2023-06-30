from flask import Flask, render_template, request, send_file
import os
import tempfile
from PyPDF2 import PdfReader
from docx import Document

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    # Get the uploaded PDF file from the request
    pdf_file = request.files['pdf_file']

    # Save the PDF file to a temporary location
    temp_dir = tempfile.mkdtemp()
    pdf_path = os.path.join(temp_dir, pdf_file.filename)
    pdf_file.save(pdf_path)

    # Create a new Word document
    doc = Document()

    # Read the PDF file and extract text
    pdf = PdfReader(pdf_path)
    for page in pdf.pages:
        text = page.extract_text()
        
        # Add the extracted text to the Word document
        doc.add_paragraph(text)

    # Save the Word document to a temporary location
    doc_path = os.path.join(temp_dir, 'converted.docx')
    doc.save(doc_path)

    # Send the converted Word file as a download
    return send_file(doc_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True,port=8000)
