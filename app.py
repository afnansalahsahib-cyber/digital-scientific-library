import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

# استخدام مجلد السيرفر المؤقت
PDF_FOLDER = '/tmp'
app.config['UPLOAD_FOLDER'] = PDF_FOLDER

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    query = request.args.get('q', '')
    
    # حماية برمجية: التأكد من وجود المجلد أو تهيئته سحابياً
    if not os.path.exists(PDF_FOLDER):
        os.makedirs(PDF_FOLDER)
        
    try:
        files = os.listdir(PDF_FOLDER)
    except Exception:
        files = []
        
    if query:
        files = [f for f in files if query.lower() in f.lower()]
    return render_template('index.html', files=files, query=query)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('index'))
    return "Invalid File Type. Only PDFs are allowed."
