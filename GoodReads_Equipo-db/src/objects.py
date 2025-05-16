## Entities

class Author:
    def __init__(self, authorid=0, author_name=None):
        self.authorid = authorid
        self.author_name = author_name

class Book:
    def __init__(self, bookid=0, title=None, isbn=None, isbn13=None,
                 language=None, publication_year=None, publisher=None,
                 num_pages=None):
        self.bookid = bookid
        self.title = title
        self.isbn = isbn
        self.isbn13 = isbn13
        self.language = language
        self.publication_year = publication_year
        self.publisher = publisher
        self.num_pages = num_pages

class Genre:
    def __init__(self, genreid=0, genre_name=None):
        self.genreid = genreid
        self.genre_name = genre_name

class Author_ID_Book_ID:
    def __init__(self, bookid=0,authorid=0):
        self.bookid = bookid
        self.authorid = authorid

class Genre_ID_Book_ID:
    def __init__(self, bookid=0,genreid=0):
        self.bookid = bookid
        self.genreid = genreid
class Review:
    def __init__(self, reviewid, userid, bookid, rating, reviewtext, reviewdate):
        self.reviewid = reviewid
        self.userid = userid
        self.bookid = bookid
        self.rating = rating
        self.reviewtext = reviewtext
        self.reviewdate = reviewdate
