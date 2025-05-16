import pandas as pd
import numpy as np
from objects import Author, Book, Genre,Author_ID_Book_ID,Genre_ID_Book_ID,Review
import db_functions
from db_functions import add_review
from utils import remove_extra_spaces
import os

## Data import
df = pd.read_csv("../data/Goodreads_books_with_genres.csv")
df_reviews= pd.read_csv("../data/goodreads_train.csv")
df = df.drop(axis=0, index=8180) # parche
df = df.drop(axis=0, index=11098) # parche
df['publication_date'] = pd.to_datetime(df['publication_date'], format='%m/%d/%Y')

# abrir conexion
db_functions.connect()

# Fill authors table
series_authors = df['Author'] # column of interest
list_authors = series_authors.str.split(pat="/").values.tolist() # convert to list (separated)
flat_list_authors = [x2 for x1 in list_authors for x2 in x1] # list flatten
array_authors_unique = pd.Series(flat_list_authors).unique()

for element in array_authors_unique:
    element = remove_extra_spaces(element)
    author = Author(author_name=element)
    db_functions.add_author(author=author)
print("Authors table filled!")

# Fill books table

book_list = list(zip(df['Book Id'],df['Title'],df['isbn'],
                       df['isbn13'],df['language_code'],df['publication_date'].dt.year,
                       df['publisher'], df['num_pages']))

for element in book_list:
    book = Book(bookid=element[0],
                title=element[1],
                isbn=element[2],
                isbn13=element[3],
                language=element[4],
                publication_year=element[5],
                publisher=element[6],
                num_pages=element[7])
    db_functions.add_book(book=book)
print("Book table filled!")


# Fill genres table
series_genres = df['genres'] # column of interest
series_genres = series_genres.dropna()   # Borramos posibles valores nan
list_genres = series_genres.str.split(r"[;,]", regex=True).values.tolist() # convert to list (separated)
flat_list_genres = [x2 for x1 in list_genres for x2 in x1] # list flatten
array_genres_unique = pd.Series(flat_list_genres).unique()

for element in array_genres_unique:
    element = remove_extra_spaces(element)
    genre = Genre(genre_name=element)
    db_functions.add_genre(genre=genre)
print("Genres table filled!")

#Fill books_authors table

    #Take author names
#series_authors = df['Author'] 
#list_authors = series_authors.str.split(pat="/").values.tolist() # convert to list (separated)
list_id_books = df['Book Id']
new_list_id_books=[] #Lista final
iD_author_unique=[]
iD_author=[] #Lista final
cc=0

    #Create list books for each author
for book in list_id_books:
    qty_list_a = len(list_authors[cc])
    for i in range(qty_list_a):
        new_list_id_books.append(book)
    cc=cc+1

print("Book Authors table filled!")


#flat_list_authors = [x2 for x1 in list_authors for x2 in x1] # list flatten
#array_authors_unique = pd.Series(flat_list_authors).unique()

cc=1

    #Create list of authors total
for iD in array_authors_unique:
    iD_author_unique.append(cc)
    cc=cc+1


for author in flat_list_authors:
    cc=0
    for author_unique in array_authors_unique:
        if author == author_unique:
            iD_author.append(iD_author_unique[cc])
        cc=cc+1

lists=zip(new_list_id_books,iD_author)
for element in lists:
    ids = Author_ID_Book_ID (bookid=element[0], authorid=element[1])
    db_functions.add_ids(ids=ids)


print("Book ID Authors ID table filled!")


#Fill books_genre table

    #Tomamos la lista de los generos sin aplanar
df_booksAndgeeneres = df[['genres','Book Id']] # columns of interest
df_booksAndgeeneres  = df_booksAndgeeneres.dropna()   # Borramos posibles valores nan
list_genres = df_booksAndgeeneres ['genres'].str.split(r"[;,]", regex=True).values.tolist() # convert to list (separated)

list_id_books = df_booksAndgeeneres ['Book Id']
new_list_id_books_g=[] #Lista final
iD_genre_unique=[]
iD_genre=[] #Lista final

cc=0
    #Create list books for each genre
for book in list_id_books:
    qty_list_g = len(list_genres[cc])
    for i in range(qty_list_g):
        new_list_id_books_g.append(book)
    cc=cc+1

#flat_list_genres = [x2 for x1 in list_genres for x2 in x1] # list flatten
#array_genres_unique = pd.Series(flat_list_genres).unique()

    #Create list of generes total
cc=1
for iD in array_genres_unique:
    iD_genre_unique.append(cc)
    cc=cc+1

for genre in flat_list_genres:
    cc=0
    for genre_unique in array_genres_unique:
        if genre == genre_unique:
            iD_genre.append(iD_genre_unique[cc])
        cc=cc+1

lists=zip(new_list_id_books_g,iD_genre)
for element in lists:
    idsgb = Genre_ID_Book_ID (bookid=element[0], genreid=element[1])
    db_functions.add_idsgb(idsgb=idsgb)


print("Book ID Genre ID table filled!")

#Fill reviews table

book_ids_in_db = set(df["Book Id"].astype(int).unique())

for _, row in df_reviews.iterrows():
    if pd.isna(row["review_id"]) or pd.isna(row["user_id"]) or pd.isna(row["book_id"]) or pd.isna(row["rating"]):
        continue

    review = Review(
        reviewid=str(row["review_id"]),
        userid=str(row["user_id"]),
        bookid=int(float(row["book_id"])),
        rating=int(float(row["rating"])),
        reviewtext=str(row["review_text"]) if pd.notna(row["review_text"]) else "",
        reviewdate=str(row["date_added"]) if pd.notna(row["date_added"]) else None
    )

    if review.bookid in book_ids_in_db:
        db_functions.add_review(review)

print("Reviews table filled!")