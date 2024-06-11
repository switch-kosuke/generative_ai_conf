from flask import Flask, request, render_template
import PyPDF2
import difflib

app = Flask(__name__)

def pdf_to_text(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = []
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text.append(page.extract_text())
    return '\n'.join(text)

def get_differences(text1, text2):
    d = difflib.HtmlDiff()
    return d.make_file(text1.splitlines(), text2.splitlines())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file1' not in request.files or 'file2' not in request.files:
        return 'No file part'

    file1 = request.files['file1']
    file2 = request.files['file2']

    if file1.filename == '' or file2.filename == '':
        return 'No selected file'

    text1 = pdf_to_text(file1)
    text2 = pdf_to_text(file2)

    differences = get_differences(text1, text2)

    return render_template('result.html', differences=differences)

if __name__ == '__main__':
    app.run(debug=True)