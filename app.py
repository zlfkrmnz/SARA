from flask import Flask, render_template, request, jsonify, redirect
from werkzeug.utils import secure_filename
import os
import sqlite3 as sql
from summarize import Summarizer
from summ import generate_summary
import fitz

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SECRET_KEY'] = 'supersecretkey'

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/explore_sara', methods=['GET', 'POST'])
def explore_sara():
    summary = None
    if request.method == 'POST':
        if 'document' not in request.files:
            return redirect(request.url)
        file = request.files['document']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            summary = summarize_document(file_path)
            save_article_to_db(filename, summary)
    articles = get_recent_articles()
    return render_template('explore_sara.html', summary=summary, articles=articles)


@app.route('/summary/<string:article_id>', methods=['GET'])
def get_summary(article_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT summary FROM articles WHERE filename = ?', (article_id,))
    result = c.fetchone()[0]
    conn.close()
    if result:
        return jsonify({'summary': result})
    else:
        return jsonify({'error': 'Article not found'}), 404


def summarize_document(file_path):
    summarizer = Summarizer("turkish-english-summarizer")
    document = fitz.open(file_path)
    text = ""
    for page_num in range(document.page_count):
        page = document.load_page(page_num)
        text += page.get_text("text")
    summarized_text = summarizer.summarize(text)
    return generate_summary(summarized_text)


def save_article_to_db(filename, summary):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO articles (filename, summary) VALUES (?, ?)', (filename, summary))
    conn.commit()
    conn.close()


def get_recent_articles():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT filename, summary FROM articles ORDER BY id DESC LIMIT 5')
    articles = c.fetchall()
    conn.close()
    return articles


def get_db_connection():
    conn = sql.connect('db/db.sqlite3')
    conn.row_factory = sql.Row
    return conn


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        # Veritabanı bağlantısını al ve verileri ekle
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO form_responses (name, email, subject, message) VALUES (?, ?, ?, ?)',
                       (name, email, subject, message))
        conn.commit()
        conn.close()

        thank_you_message = f"Thank you {name}, your message has been sent."
        return jsonify(message=thank_you_message)


if __name__ == '__main__':
    app.run(debug=True)
