# DATABASE LAYER

import sqlite3 as sql
from contextlib import closing
from objects import Author, Book,Author_ID_Book_ID,Genre,Genre_ID_Book_ID

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

def get_author(author_id):
    """
    Retrieves an author from the Authors table by their ID.

    Args:
        author_id: The ID of the author to retrieve.

    Returns:
        An Author object if found, None otherwise.
    """
    sql_query = "SELECT AuthorID, AuthorName FROM Authors WHERE AuthorID = ?"
    with closing(conn.cursor()) as cursor:
        cursor.execute(sql_query, (author_id,))
        row = cursor.fetchone()
        if row:
            return Author(authorid=row['AuthorID'], author_name=row['AuthorName'])
        else:
            return None

def update_author(author):
    """
    Updates an existing author's information in the Authors table.

    Args:
        author: An Author object with the updated information.  The AuthorID is used to identify the author to update.
    """
    sql_query = "UPDATE Authors SET AuthorName = ? WHERE AuthorID = ?"
    with closing(conn.cursor()) as cursor:
        cursor.execute(sql_query, (author.author_name, author.authorid))
        conn.commit()

def delete_author(author_id):
    """
    Deletes an author from the Authors table by their ID.

    Args:
        author_id: The ID of the author to delete.
    """
    sql_query = "DELETE FROM Authors WHERE AuthorID = ?"
    with closing(conn.cursor()) as cursor:
        cursor.execute(sql_query, (author_id,))
        conn.commit()

def get_all_authors():
    """
    Retrieves all authors from the Authors table.

    Returns:
        A list of Author objects.
    """
    sql_query = "SELECT AuthorID, AuthorName FROM Authors"
    with closing(conn.cursor()) as cursor:
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        return [Author(authorid=row['AuthorID'], author_name=row['AuthorName']) for row in rows]



### Book functions

def add_book(book): # needs an object that represents all of the information of the author
    sql_query = '''INSERT OR IGNORE INTO Books (BookID, Title, ISBN, ISBN13, Language, PublicationYear, Publisher, NumPages)
    VALUES (?,?,?,?,?,?,?,?)'''
    with closing(conn.cursor()) as cursor:
        cursor.execute(sql_query, (book.bookid, book.title, book.isbn, book.isbn13,
                                   book.language, book.publication_year, book.publisher,
                                   book.num_pages)) # representa al objeto employee
        conn.commit()

def get_book(book_id):
    """
    Retrieves a book from the Books table by its ID.

    Args:
        book_id: The ID of the book to retrieve.

    Returns:
        A Book object if found, otherwise None.
    """
    sql_query = "SELECT BookID, Title, ISBN, ISBN13, Language, PublicationYear, Publisher, NumPages FROM Books WHERE BookID = ?"
    with closing(conn.cursor()) as cursor:
        cursor.execute(sql_query, (book_id,))
        row = cursor.fetchone()
        if row:
            return Book(bookid=row[0], title=row[1], isbn=row[2], isbn13=row[3],
                        language=row[4], publication_year=row[5], publisher=row[6], num_pages=row[7])
        return None

def update_book(book):
    """
    Updates an existing book's information in the Books table.

    Args:
        book: A Book object with the updated information. The BookID is used to identify the book to update.
    """
    sql_query = '''UPDATE Books SET Title = ?, ISBN = ?, ISBN13 = ?, Language = ?,
                   PublicationYear = ?, Publisher = ?, NumPages = ? WHERE BookID = ?'''
    with closing(conn.cursor()) as cursor:
        cursor.execute(sql_query, (book.title, book.isbn, book.isbn13, book.language,
                                   book.publication_year, book.publisher, book.num_pages, book.bookid))
        conn.commit()

def delete_book(book_id):
    """
    Deletes a book from the Books table by its ID.

    Args:
        book_id: The ID of the book to delete.
    """
    sql_query = "DELETE FROM Books WHERE BookID = ?"
    with closing(conn.cursor()) as cursor:
        cursor.execute(sql_query, (book_id,))
        conn.commit()

def get_all_books():
    """
    Retrieves all books from the Books table.

    Returns:
        A list of Book objects.
    """
    sql_query = "SELECT BookID, Title, ISBN, ISBN13, Language, PublicationYear, Publisher, NumPages FROM Books"
    with closing(conn.cursor()) as cursor:
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        return [Book(bookid=row[0], title=row[1], isbn=row[2], isbn13=row[3],
                     language=row[4], publication_year=row[5], publisher=row[6], num_pages=row[7]) for row in rows]



### Genre functions

def add_genre(genre): # needs an object that represents all of the information of the author
    sql_query = '''INSERT OR IGNORE INTO Genres (GenreName)
    VALUES (?)'''
    with closing(conn.cursor()) as cursor:
        cursor.execute(sql_query, (genre.genre_name,)) # representa al objeto employee
        conn.commit()

def get_genre(genre_id):
    """
    Retrieves a genre from the Genres table by its ID.

    Args:
        genre_id: The ID of the genre to retrieve.

    Returns:
        A Genre object if found, otherwise None.
    """
    sql_query = "SELECT GenreID, GenreName FROM Genres WHERE GenreID = ?"
    with closing(conn.cursor()) as cursor:
        cursor.execute(sql_query, (genre_id,))
        row = cursor.fetchone()
        if row:
            return Genre(genreid=row[0], genre_name=row[1])
        return None

def update_genre(genre):
    """
    Updates an existing genre's information in the Genres table.

    Args:
        genre: A Genre object with the updated information. The GenreID is used to identify the genre to update.
    """
    sql_query = "UPDATE Genres SET GenreName = ? WHERE GenreID = ?"
    with closing(conn.cursor()) as cursor:
        cursor.execute(sql_query, (genre.genre_name, genre.genreid))
        conn.commit()

def delete_genre(genre_id):
    """
    Deletes a genre from the Genres table by its ID.

    Args:
        genre_id: The ID of the genre to delete.
    """
    sql_query = "DELETE FROM Genres WHERE GenreID = ?"
    with closing(conn.cursor()) as cursor:
        cursor.execute(sql_query, (genre_id,))
        conn.commit()

def get_all_genres():
    """
    Retrieves all genres from the Genres table.

    Returns:
        A list of Genre objects.
    """
    sql_query = "SELECT GenreID, GenreName FROM Genres"
    with closing(conn.cursor()) as cursor:
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        return [Genre(genreid=row[0], genre_name=row[1]) for row in rows]
    
### Author Book IDs functions

def add_ids(ids): # needs an object that represents all of the information of the author
    sql_query = '''INSERT OR IGNORE INTO BookAuthors (BookID, AuthorID)
    VALUES (?,?)'''
    with closing(conn.cursor()) as cursor:
        cursor.execute(sql_query, (ids.bookid,ids.authorid)) # representa al objeto employee
        conn.commit()


### Genre Book IDs functions
def add_idsgb(idsgb): # needs an object that represents all of the information of the author
    sql_query = '''INSERT OR IGNORE INTO BookGenres (BookID, GenreID)
    VALUES (?,?)'''
    with closing(conn.cursor()) as cursor:
        cursor.execute(sql_query, (idsgb.bookid,idsgb.genreid)) # representa al objeto employee
        conn.commit()