# Goodreads-db

A SQLite database project for Goodreads book data analysis.

## Project Overview

This project creates and populates a SQLite database with Goodreads book data. It includes functionality for storing and querying information about books, authors, genres, users, ratings, and reviews.


This project is a desktop application developed in Python using the Tkinter library to manage a Goodreads book database. The application allows performing CRUD (Create, Read, Update, Delete) operations on the Books and Authors tables of the SQLite database.


## Project Structure

- `/data`: Contains the source data files
  - `goodreads_test.csv`: Test dataset
  - `goodreads_book_works.json`: Book works data in JSON format
  - `Goodreads_books_with_genres.csv`: Books with genre information

- `/db`: Directory for the SQLite database file
  - The database is created as `goodreads-db.sqlite`

- `/src`: Source code for database creation and operations
  - `create_db.py`: Creates the database schema with tables for books, authors, genres, users, ratings, and reviews
  - `db_fill.py`: Populates the database with data from CSV files
  - `db_functions.py`: Helper functions for database operations
  - `objects.py`: Object definitions for books, authors, etc.
  - `utils.py`: Utility functions
  -   `gui.py`: Implements the graphical user interface using Tkinter, allowing users to interact with the database through tabs for Books and Authors (and now Genres).

- `/notebooks`: Jupyter notebooks for data exploration
  - `Goodreads-db-exploration.ipynb`: Notebook for exploring the database

## Database Schema

The database consists of the following tables:

- `Books`: Book information (ID, title, ISBN, language, publication year, etc.)
- `Authors`: Author information
- `BookAuthors`: Many-to-many relationship between books and authors
- `Genres`: Genre categories
- `BookGenres`: Many-to-many relationship between books and genres
- `Users`: User information
- `Ratings`: User ratings for books
- `Reviews`: User reviews for books

## Getting Started

1. Clone this repository
2. Ensure you have Python installed with the required packages (pandas, numpy, sqlite3)
3. Run `python src/create_db.py` to create the database schema
4. Run `python src/db_fill.py` to populate the database with data
5. Use the Jupyter notebook for data exploration and analysis
6. Run `python src/db_fill.py` to display the interface and manipulate the data with the CRUD functons

## Usage

The database can be used for various analyses of book data, including:
- Book recommendation systems
- Genre analysis
- Author popularity metrics
- Rating distribution analysis
- User behavior analysis

## Graphical Interface Features

The graphical interface (`gui.py`) provides the following functionalities through separate tabs:

### Books Tab

-   Allows entering details for a new book (Book ID, Title, ISBN, ISBN13, Language, Publication Year, Publisher, Number of Pages).
-   Buttons for:
    -   **Add Book**: Inserts a new book into the database.
    -   **Get Book**: Searches for a book by its Book ID and displays its details in the fields.
    -   **Update Book**: Modifies the details of an existing book (identified by its Book ID).
    -   **Delete Book**: Removes a book from the database by its Book ID.
-   Basic validation of the fields (required fields and data types for year and number of pages).

### Authors Tab

-   Allows entering the name of a new author (Author ID, Author Name).
-   Buttons for:
    -   **Add Author**: Inserts a new author into the database.
    -   **Get Author**: Searches for an author by their Author ID and displays their name in the field.
    -   **Update Author**: Modifies the name of an existing author (identified by their Author ID).
    -   **Delete Author**: Removes an author from the database by their Author ID.
-   Basic validation of the author name field.

### Genres Tab

-   Allows entering the name of a new genre (Genre ID, Genre Name).
-   Buttons for:
    -   **Add Genre**: Inserts a new genre into the database.
    -   **Get Genre**: Searches for a genre

## Requirements

- Python 3.x
- pandas
- numpy
- sqlite3
- Jupyter (for notebooks)




