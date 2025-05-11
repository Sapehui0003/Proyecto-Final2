# DATABASE LAYER

import sqlite3 as sql
from contextlib import closing
from objects import Author, Book

# Variable global que representa el string de conexion
conn = None

# Vamos a necesitar varios métodos
# Autores

def connect():
    global conn
    if not conn: # if conn has not been set then set
        conn =sql.connect("../db/goodreads-db.sqlite")
        conn.row_factory = sql.Row # returns a dict instead of a tuple
        
def close():
    if conn:
        conn.close()
    # we call from de ui moduls when the user terminate the application

### Author functions

def add_author(author): # needs an object that represents all of the information of the author
    sql_query = '''INSERT OR IGNORE INTO Authors (AuthorName)
    VALUES (?)'''
    with closing(conn.cursor()) as cursor:
        cursor.execute(sql_query, (author.author_name,)) # representa al objeto employee
        conn.commit()

### Book functions

def add_book(book): # needs an object that represents all of the information of the author
    sql_query = '''INSERT OR IGNORE INTO Books (BookID, Title, ISBN, ISBN13, Language, PublicationYear, Publisher, NumPages)
    VALUES (?,?,?,?,?,?,?,?)'''
    with closing(conn.cursor()) as cursor:
        cursor.execute(sql_query, (book.bookid, book.title, book.isbn, book.isbn13,
                                   book.language, book.publication_year, book.publisher,
                                   book.num_pages)) # representa al objeto employee
        conn.commit()

#Book genre functions
def add_book_genre(book_id, genre_id):
    """
    Adds a relationship between a book and a genre to the BookGenres table.

    Args:
        book_id: The ID of the book.
        genre_id: The ID of the genre.
    """
    sql_query = '''INSERT OR IGNORE INTO BookGenres (BookID, GenreID)
    VALUES (?,?)'''
    with closing(conn.cursor()) as cursor:
        cursor.execute(sql_query, (book_id, genre_id))
        conn.commit()

def get_book_genres(book_id):
    """
    Retrieves all genre IDs for a given book ID from the BookGenres table.

    Args:
        book_id: The ID of the book.

    Returns:
        A list of genre IDs associated with the book.  Returns an empty list if no genres are found.
    """
    sql_query = '''SELECT GenreID FROM BookGenres WHERE BookID = ?'''
    with closing(conn.cursor()) as cursor:
        cursor.execute(sql_query, (book_id,))
        results = cursor.fetchall()  # Fetch all matching rows
        return [row['GenreID'] for row in results] # Extract GenreIDs

def delete_book_genre(book_id, genre_id):
    """
    Deletes a specific book-genre relationship from the BookGenres table.

    Args:
        book_id: The ID of the book.
        genre_id: The ID of the genre to delete.
    """
    sql_query = '''DELETE FROM BookGenres WHERE BookID = ? AND GenreID = ?'''
    with closing(conn.cursor()) as cursor:
        cursor.execute(sql_query, (book_id, genre_id))
        conn.commit()

def update_book_genres(book_id, genre_ids):
    """
    Updates the genres for a given book in the BookGenres table.

    This function efficiently manages adding and removing genres to ensure the database
    reflects the provided list of genre IDs for the specified book.

    Args:
        book_id: The ID of the book to update.
        genre_ids: A list of Genre IDs that should be associated with the book.
    """
    # 1. Get the current genre IDs for the book.
    existing_genre_ids = get_book_genres(book_id)

    # 2. Determine genres to add and remove.
    genres_to_add = set(genre_ids) - set(existing_genre_ids)
    genres_to_remove = set(existing_genre_ids) - set(genre_ids)

    # 3. Add new genres.
    for genre_id in genres_to_add:
        add_book_genre(book_id, genre_id)

    # 4. Remove old genres.
    for genre_id in genres_to_remove:
        delete_book_genre(book_id, genre_id)