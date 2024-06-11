import csv
import hashlib
import json
import math
from io import BytesIO, StringIO
from math import ceil

from flask import Blueprint, render_template, request, send_file, Response, flash, redirect, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from app import db_operation
import asyncio

from S3Client import S3Client

bp = Blueprint('books', __name__, url_prefix='/books')

MAX_PER_PAGE = 1

s3_client = S3Client(
    access_key="YCAJEy9QLKnVTXGqdO6xlh_44",
    secret_key="YCOnxag0SsrhXf96gp9ap6vQSoPIG6QilKQ7zU0b",
    endpoint_url="https://storage.yandexcloud.net",
    bucket_name="mnikishaev",
)


# Routes
@bp.route('/')
@db_operation
@login_required

def index(cursor):
    page = request.args.get('page', 1, type=int)
    offset = (page - 1) * MAX_PER_PAGE

    cursor.execute("SELECT COUNT(*) as count FROM books")
    total_books = cursor.fetchone()[0]

    cursor.execute("""
            SELECT b.*, bc.file_name, 
                   GROUP_CONCAT(g.name SEPARATOR ', ') as genres, 
                   AVG(r.rating) as avg_rating, 
                   COUNT(r.id) as review_count
            FROM books b
            LEFT JOIN book_covers bc ON b.cover_id = bc.id
            LEFT JOIN book_genres bg ON b.id = bg.book_id
            LEFT JOIN genres g ON bg.genre_id = g.id
            LEFT JOIN reviews r ON b.id = r.book_id
            GROUP BY b.id
            ORDER BY b.year DESC
            LIMIT %s OFFSET %s
        """, (MAX_PER_PAGE, offset))
    books = cursor.fetchall()

    res = []
    for book in books:
        book_dict = book._asdict()
        res.append(book_dict)

    for book in res:
        filename = book['file_name']
        if filename:
            file_data = asyncio.run(s3_client.get_file(filename))
            if file_data:
                book['background_image'] = file_data

    page_count = math.ceil(total_books / MAX_PER_PAGE)
    pages = range(1, page_count + 1)

    return render_template('books/index.html', books=res, pages=pages, page=page, page_count=page_count)


# @bp.route('/create', methods=['GET', 'POST'])
# @db_operation
# @login_required
# def create_book(cursor):
#     if request.method == 'POST':
#         # Get form data
#         title = request.form.get('title')
#         author = request.form.get('author')
#         description = request.form.get('description')
#         year = request.form.get('year')
#         publisher = request.form.get('publisher')
#         pages = request.form.get('pages')
#         genres_selected = request.form.getlist('genre')  # Get selected genres as list
#
#         # file = request.files.get('file')
#         # if file and file.filename != '':
#         #     filename = secure_filename(file.filename)
#         #     try:
#         #         asyncio.run(s3_client.upload_file_v2(file.stream, filename))
#         #         flash('File uploaded successfully', 'success')
#         #     except Exception as e:
#         #         flash(f'Error uploading file: {e}', 'error')
#
#
#         print("Title:", title)
#         print("Author:", author)
#         print("Description:", description)
#         print("Year:", year)
#         print("Publisher:", publisher)
#         print("Pages:", pages)
#         print("Selected Genres:", genres_selected)
#
#         return "Book created successfully!"  # You can redirect or render a different template here
#     else:
#         query = "SELECT * FROM genres"
#         cursor.execute(query)
#         res = cursor.fetchall()
#
#         return render_template('books/create.html', genres=res)

@bp.route('/create', methods=['GET', 'POST'])
@db_operation
@login_required
def create(cursor):
    if request.method == 'POST':
        # Get form data
        title = request.form.get('title')
        author = request.form.get('author')
        description = request.form.get('description')
        year = request.form.get('year')
        publisher = request.form.get('publisher')
        pages = request.form.get('pages')
        genres_selected = request.form.getlist('genre')

        cover_id = None
        background_image = request.files.get('background_image')
        print(background_image)

        if background_image and background_image.filename != '':
            filename = secure_filename(background_image.filename)
            file_content = background_image.read()
            md5_hash = hashlib.md5(file_content).hexdigest()
            mime_type = background_image.mimetype

            cursor.execute("""
                INSERT INTO book_covers (file_name, mime_type, md5_hash)
                VALUES (%s, %s, %s)
            """, (filename, mime_type, md5_hash))
            cover_id = cursor.lastrowid

            background_image.stream.seek(0)
            asyncio.run(s3_client.upload_file_v2(background_image.stream, filename))
        else:
            print("NO IMAGE")
        cursor.execute("""
            INSERT INTO books (title, description, year, publisher, author, pages, cover_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (title, description, year, publisher, author, pages, cover_id))
        book_id = cursor.lastrowid

        for genre_id in genres_selected:
            cursor.execute("""
                INSERT INTO book_genres (book_id, genre_id)
                VALUES (%s, %s)
            """, (book_id, genre_id))

        flash("Book created successfully!", "success")
        return redirect(url_for('books.create'))

    cursor.execute("SELECT * FROM genres")
    genres = cursor.fetchall()
    book_data = {
        "genres": []
    }
    return render_template('books/create.html', genres=genres, book_data=book_data)


@bp.route('/update/<int:book_id>', methods=['GET', 'POST'])
@db_operation
@login_required
def update(cursor, book_id):
    if request.method == 'POST':
        # Get form data
        title = request.form.get('title')
        author = request.form.get('author')
        description = request.form.get('description')
        year = request.form.get('year')
        publisher = request.form.get('publisher')
        pages = request.form.get('pages')
        genres_selected = request.form.getlist('genre')

        # Update book details in the database
        cursor.execute("""
            UPDATE books
            SET title = %s, description = %s, year = %s, publisher = %s, author = %s, pages = %s
            WHERE id = %s
        """, (title, description, year, publisher, author, pages, book_id))

        # Update genres
        cursor.execute("""
            DELETE FROM book_genres WHERE book_id = %s
        """, (book_id,))

        for genre_id in genres_selected:
            cursor.execute("""
                INSERT INTO book_genres (book_id, genre_id)
                VALUES (%s, %s)
            """, (book_id, genre_id))

        flash("Book updated successfully!", "success")
        return redirect(url_for('books.index'))

    # Fetch the existing book details
    cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
    book = cursor.fetchone()

    if not book:
        flash("Book not found.", "error")
        return redirect(url_for('books.index'))

    # Fetch genres
    cursor.execute("SELECT * FROM genres")
    genres = cursor.fetchall()

    cursor.execute("SELECT genre_id FROM book_genres WHERE book_id = %s", (book_id,))
    selected_genres = cursor.fetchall()

    book_dict = book._asdict()
    book_dict["selected_genres"] = [id[0] for id in selected_genres]
    print(book_dict)
    return render_template('books/update.html', genres=genres, book_data=book_dict, book_id=book_id)

# @app.route('/book/<int:book_id>')
# def view_book(book_id):
#     # Fetch book details from database
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT * FROM books WHERE id = %s", (book_id,))
#     book = cur.fetchone()
#     cur.execute("SELECT * FROM reviews WHERE book_id = %s", (book_id,))
#     reviews = cur.fetchall()
#     cur.close()
#     return render_template('book.html', book=book, reviews=reviews)
#
# @app.route('/add_review/<int:book_id>', methods=['GET', 'POST'])
# def add_review(book_id):
#     if request.method == 'POST':
#         rating = request.form['rating']
#         review_text = request.form['review_text']
#         # Save review to database
#         cur = mysql.connection.cursor()
#         cur.execute("INSERT INTO reviews (book_id, user_id, rating, text) VALUES (%s, %s, %s, %s)",
#                     (book_id, session['user_id'], rating, review_text))
#         mysql.connection.commit()
#         cur.close()
#         flash('Review added successfully', 'success')
#         return redirect(url_for('view_book', book_id=book_id))
#     return render_template('add_review.html', book_id=book_id)

# Other routes for login, logout, etc. would go here
