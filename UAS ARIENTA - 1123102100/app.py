from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import os
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'library_secret'
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    print(f"Folder '{UPLOAD_FOLDER}' berhasil dibuat.")

# Database initialization
DATABASE = 'library.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            category TEXT NOT NULL,
            image TEXT,
            stock INTEGER DEFAULT 0
        )
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
        """)
        conn.commit()

# Route Index
@app.route('/')
def index():
    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, title, author, category, image FROM books")
        books = cur.fetchall()
    return render_template('index.html', books=books)

# Route Detail Buku
@app.route('/detail/<int:book_id>')
def detail(book_id):
    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM books WHERE id=?", (book_id,))
        book = cur.fetchone()
    if not book:
        flash("Buku tidak ditemukan!", "danger")
        return redirect(url_for('index'))
    return render_template('detail.html', book=book)

# Admin Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Validasi username dan password secara statis
        if username == 'arin' and password == 'admin':
            session['username'] = username
            return redirect(url_for('admin'))
        
        # Jika username atau password salah
        flash('Username atau password salah!', 'danger')
    
    return render_template('login.html')

# Admin Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Berhasil logout.', 'success')
    return redirect(url_for('index'))

# Admin Panel
@app.route('/admin')
def admin():
    if 'username' not in session:
        flash('Harap login terlebih dahulu!', 'danger')
        return redirect(url_for('login'))
    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM books")
        books = cur.fetchall()
    return render_template('admin.html', books=books)

# Tambah Buku
@app.route('/admin/add', methods=['GET', 'POST'])
def add_book():
    if 'username' not in session:
        flash('Harap login terlebih dahulu!', 'danger')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form['judul']
        author = request.form['penulis']
        category = request.form['kategori']
        stock = int(request.form['stok'])  # Ambil data stok dari form
        image = request.files['gambar']
        image_path = None

        if image:
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            filename = f"{timestamp}_{image.filename}"
            local_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(local_path)
            image_path = f"{UPLOAD_FOLDER}/{filename}".replace('\\', '/')
        
        with sqlite3.connect(DATABASE) as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO books (title, author, category, image, stock) VALUES (?, ?, ?, ?, ?)", 
                        (title, author, category, image_path, stock))
            conn.commit()

        flash('Buku berhasil ditambahkan!', 'success')
        return redirect(url_for('admin'))

    return render_template('add.html')

# Edit Buku
# Edit Buku
@app.route('/admin/edit/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    if 'username' not in session:
        flash('Harap login terlebih dahulu!', 'danger')
        return redirect(url_for('login'))
    
    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM books WHERE id=?", (book_id,))
        book = cur.fetchone()
    
    if not book:
        flash('Buku tidak ditemukan!', 'danger')
        return redirect(url_for('admin'))
    
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        category = request.form['category']
        stock = int(request.form['stok'])  # Ambil data stok dari form
        
        with sqlite3.connect(DATABASE) as conn:
            cur = conn.cursor()
            cur.execute("""
            UPDATE books SET title=?, author=?, category=?, stock=? WHERE id=?
            """, (title, author, category, stock, book_id))
            conn.commit()
        
        flash('Buku berhasil diperbarui!', 'success')
        return redirect(url_for('admin'))
    
    return render_template('edit.html', book=book)
    
# Hapus Buku
@app.route('/admin/delete/<int:book_id>')
def delete_book(book_id):
    if 'username' not in session:
        flash('Harap login terlebih dahulu!', 'danger')
        return redirect(url_for('login'))
    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM books WHERE id=?", (book_id,))
        conn.commit()
    flash('Buku berhasil dihapus!', 'success')
    return redirect(url_for('admin'))

@app.route('/kategori')
def kategori():
    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT category FROM books")
        categories = cur.fetchall()
    cleaned_categories = [category[0] for category in categories]
    return render_template('kategori.html', categories=cleaned_categories)

# Route untuk menampilkan buku berdasarkan kategori
@app.route('/kategori/<string:category_name>')
def books_by_category(category_name):
    print(f"Category received: {category_name}")  # Debugging
    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, title, author, category, image FROM books WHERE category=?", (category_name,))
        books = cur.fetchall()
    print(f"Books found: {books}")  # Debugging
    return render_template('books_by_category.html', category=category_name, books=books)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
