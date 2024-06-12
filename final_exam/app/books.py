import asyncio
import hashlib
import logging
import math
import os

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from werkzeug.utils import secure_filename

from S3Client import S3Client
from app import db_operation
from auto import check_for_privelege

bp = Blueprint('books', __name__, url_prefix='/books')

MAX_PER_PAGE = 10

s3_client = S3Client(
    access_key=os.getenv("S3_ACCESS_KEY"),
    secret_key=os.getenv("S3_SECRET_KEY"),
    endpoint_url="https://storage.yandexcloud.net",
    bucket_name="mnikishaev",
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_books_with_pagination(offset, cursor):
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
    return cursor.fetchall()


def handle_book_cover(background_image, cursor):
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
        s3_client.upload_file_v2(background_image.stream, filename)

        return cover_id
    return None


def insert_book_genres(book_id, genres_selected, cursor):
    data = [(book_id, genre_id) for genre_id in genres_selected]
    insert_statement = """
            INSERT INTO book_genres (book_id, genre_id)
            VALUES (%s, %s)
        """
    cursor.executemany(insert_statement, data)


async def add_background_images(books):
    for book in books:
        filename = book['file_name']
        if filename:
            file_data = await s3_client.get_file(filename)
            if file_data:
                book['background_image'] = file_data


@bp.route('/')
@db_operation
@login_required
def index(cursor):
    page = request.args.get('page', 1, type=int)
    offset = (page - 1) * MAX_PER_PAGE

    cursor.execute("SELECT COUNT(*) as count FROM books")
    total_books = cursor.fetchone()[0]

    books = get_books_with_pagination(offset, cursor)
    logger.info(f'Fetched: {len(books)} books')
    books = [book._asdict() for book in books]

    asyncio.run(add_background_images(books))

    page_count = math.ceil(total_books / MAX_PER_PAGE)
    pages = range(1, page_count + 1)

    return render_template('books/index.html', books=books, pages=pages, page=page, page_count=page_count)


@bp.route('/create', methods=['GET', 'POST'])
@db_operation
@login_required
@check_for_privelege('create')
def create(cursor):
    fields = ['title', 'author', 'description', 'year', 'publisher', 'pages']
    if request.method == 'POST':
        book_data = {field: request.form.get(field) for field in fields}
        genres_selected = request.form.getlist('genre')
        background_image = request.files.get('background_image')
        cover_id = handle_book_cover(background_image, cursor)

        cursor.execute("""
            INSERT INTO books (title, description, year, publisher, author, pages, cover_id)
            VALUES (%(title)s, %(description)s, %(year)s, %(publisher)s, %(author)s, %(pages)s, %(cover_id)s)
        """, {**book_data, 'cover_id': cover_id})
        book_id = cursor.lastrowid
        insert_book_genres(book_id, genres_selected, cursor)

        flash("Книга успешно добавлена!", "success")
        return redirect(url_for('books.index'))

    cursor.execute("SELECT * FROM genres")
    genres = cursor.fetchall()
    return render_template('books/create.html', genres=genres, book_data={"genres": []})


@bp.route('/update/<int:book_id>', methods=['GET', 'POST'])
@db_operation
@login_required
@check_for_privelege('update')
def update(cursor, book_id):
    if request.method == 'POST':
        fields = ['title', 'author', 'description', 'year', 'publisher', 'pages']
        book_data = {field: request.form.get(field) for field in fields}
        genres_selected = request.form.getlist('genre')

        cursor.execute("""
                    UPDATE books
                    SET title = %(title)s, description = %(description)s, year = %(year)s, publisher = %(publisher)s,
                    author = %(author)s, pages = %(pages)s
                    WHERE id = %(book_id)s
                """, {**book_data, 'book_id': book_id})

        cursor.execute("""
            DELETE FROM book_genres WHERE book_id = %s
        """, (book_id,))

        insert_book_genres(book_id, genres_selected, cursor)

        flash("Книга успешно обновлена!", "success")
        return redirect(url_for('books.index'))

    cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
    book = cursor.fetchone()
    if not book:
        flash("Книга не найдена.", "error")
        return redirect(url_for('books.index'))

    cursor.execute("SELECT * FROM genres")
    genres = cursor.fetchall()

    cursor.execute("SELECT genre_id FROM book_genres WHERE book_id = %s", (book_id,))
    selected_genres = cursor.fetchall()

    book_dict = book._asdict()
    book_dict["selected_genres"] = [id[0] for id in selected_genres]
    return render_template('books/update.html', genres=genres, book_data=book_dict, book_id=book_id)


@bp.route('/view/<int:book_id>')
@db_operation
@login_required
def view(cursor, book_id):
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
        WHERE b.id = %s
        GROUP BY b.id
    """, (book_id,))
    book = cursor.fetchone()

    if not book:
        flash("Книга не найдена", "warning")
        return redirect(url_for('books.index'))

    book_dict = book._asdict()

    filename = book_dict.get('file_name')
    if filename:
        file_data = asyncio.run(s3_client.get_file(filename))
        if file_data:
            book_dict['background_image'] = file_data

    return render_template('books/view.html', book=book_dict)


@bp.route('/delete/<int:book_id>', methods=['POST'])
@db_operation
@login_required
@check_for_privelege('delete')
def delete(cursor, book_id):
    cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
    book = cursor.fetchone()

    if not book:
        flash("Книга не найдена", "warning")
        return redirect(url_for('books.index'))

    cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
    cursor.execute("DELETE FROM book_genres WHERE book_id = %s", (book_id,))
    cursor.execute("DELETE FROM reviews WHERE book_id = %s", (book_id,))

    flash("Book deleted successfully!", "success")
    return redirect(url_for('books.index'))
