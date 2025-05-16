# gui.py
import tkinter as tk
from tkinter import ttk, messagebox
import db_functions
from objects import Author, Book, Genre

class GoodreadsApp:
    def __init__(self, master):
        self.master = master
        master.title("Goodreads Database Manager")

        db_functions.connect()  # Conectar a la base de datos al iniciar la aplicación

        self.notebook = ttk.Notebook(master)
        self.notebook.pack(pady=10, padx=10, expand=True, fill='both')

        self.create_books_tab()
        self.create_authors_tab()
        self.create_genres_tab()
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        if messagebox.askokcancel("Salir", "¿Estás seguro de que quieres salir?"):
            db_functions.close()
            self.master.destroy()

    # ---------------------- TABLA BOOKS ----------------------
    def create_books_tab(self):
        self.books_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.books_tab, text='Libros')

        # Campos para agregar/actualizar libro
        ttk.Label(self.books_tab, text="Book ID:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.book_id_entry = ttk.Entry(self.books_tab)
        self.book_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        ttk.Label(self.books_tab, text="Título:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.book_title_entry = ttk.Entry(self.books_tab)
        self.book_title_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        ttk.Label(self.books_tab, text="ISBN:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.book_isbn_entry = ttk.Entry(self.books_tab)
        self.book_isbn_entry.grid(row=2, column=1, padx=5, pady=5, sticky='ew')

        ttk.Label(self.books_tab, text="ISBN13:").grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.book_isbn13_entry = ttk.Entry(self.books_tab)
        self.book_isbn13_entry.grid(row=3, column=1, padx=5, pady=5, sticky='ew')

        ttk.Label(self.books_tab, text="Idioma:").grid(row=4, column=0, padx=5, pady=5, sticky='w')
        self.book_language_entry = ttk.Entry(self.books_tab)
        self.book_language_entry.grid(row=4, column=1, padx=5, pady=5, sticky='ew')

        ttk.Label(self.books_tab, text="Año de Publicación:").grid(row=5, column=0, padx=5, pady=5, sticky='w')
        self.book_publication_year_entry = ttk.Entry(self.books_tab)
        self.book_publication_year_entry.grid(row=5, column=1, padx=5, pady=5, sticky='ew')

        ttk.Label(self.books_tab, text="Editorial:").grid(row=6, column=0, padx=5, pady=5, sticky='w')
        self.book_publisher_entry = ttk.Entry(self.books_tab)
        self.book_publisher_entry.grid(row=6, column=1, padx=5, pady=5, sticky='ew')

        ttk.Label(self.books_tab, text="Número de Páginas:").grid(row=7, column=0, padx=5, pady=5, sticky='w')
        self.book_num_pages_entry = ttk.Entry(self.books_tab)
        self.book_num_pages_entry.grid(row=7, column=1, padx=5, pady=5, sticky='ew')

        # Botones para operaciones de libros
        ttk.Button(self.books_tab, text="Agregar Libro", command=self.add_book).grid(row=8, column=0, padx=5, pady=10, sticky='ew')
        ttk.Button(self.books_tab, text="Obtener Libro", command=self.get_book).grid(row=8, column=1, padx=5, pady=10, sticky='ew')
        ttk.Button(self.books_tab, text="Actualizar Libro", command=self.update_book).grid(row=9, column=0, padx=5, pady=10, sticky='ew')
        ttk.Button(self.books_tab, text="Eliminar Libro", command=self.delete_book).grid(row=9, column=1, padx=5, pady=10, sticky='ew')

    def add_book(self):
        title = self.book_title_entry.get()
        isbn = self.book_isbn_entry.get()
        isbn13 = self.book_isbn13_entry.get()
        language = self.book_language_entry.get()
        publication_year = self.book_publication_year_entry.get()
        publisher = self.book_publisher_entry.get()
        num_pages = self.book_num_pages_entry.get()
        if title and publication_year and publisher and num_pages:
            try:
                year = int(publication_year)
                pages = int(num_pages)
                book = Book(title=title, isbn=isbn, isbn13=isbn13, language=language,
                            publication_year=year, publisher=publisher, num_pages=pages)
                db_functions.add_book(book=book)
                messagebox.showinfo("Éxito", f"Libro '{title}' agregado.")
                self.clear_book_fields()
            except ValueError:
                messagebox.showerror("Error", "Año de publicación y número de páginas deben ser números enteros.")
        else:
            messagebox.showerror("Error", "Título, año de publicación, editorial y número de páginas son obligatorios.")

    def get_book(self):
        book_id_str = self.book_id_entry.get()
        if book_id_str:
            try:
                book_id = int(book_id_str)
                book = db_functions.get_book(book_id)
                if book:
                    self.book_title_entry.delete(0, tk.END)
                    self.book_title_entry.insert(0, book.title)
                    self.book_isbn_entry.delete(0, tk.END)
                    self.book_isbn_entry.insert(0, book.isbn)
                    self.book_isbn13_entry.delete(0, tk.END)
                    self.book_isbn13_entry.insert(0, book.isbn13)
                    self.book_language_entry.delete(0, tk.END)
                    self.book_language_entry.insert(0, book.language)
                    self.book_publication_year_entry.delete(0, tk.END)
                    self.book_publication_year_entry.insert(0, book.publication_year)
                    self.book_publisher_entry.delete(0, tk.END)
                    self.book_publisher_entry.insert(0, book.publisher)
                    self.book_num_pages_entry.delete(0, tk.END)
                    self.book_num_pages_entry.insert(0, book.num_pages)
                else:
                    messagebox.showinfo("Información", f"No se encontró ningún libro con ID {book_id}.")
            except ValueError:
                messagebox.showerror("Error", "El ID del libro debe ser un número entero.")
        else:
            messagebox.showerror("Error", "Por favor, introduce el ID del libro a buscar.")

    def update_book(self):
        book_id_str = self.book_id_entry.get()
        title = self.book_title_entry.get()
        isbn = self.book_isbn_entry.get()
        isbn13 = self.book_isbn13_entry.get()
        language = self.book_language_entry.get()
        publication_year = self.book_publication_year_entry.get()
        publisher = self.book_publisher_entry.get()
        num_pages = self.book_num_pages_entry.get()
        if book_id_str and title and publication_year and publisher and num_pages:
            try:
                book_id = int(book_id_str)
                year = int(publication_year)
                pages = int(num_pages)
                book = Book(bookid=book_id, title=title, isbn=isbn, isbn13=isbn13, language=language,
                            publication_year=year, publisher=publisher, num_pages=pages)
                db_functions.update_book(book=book)
                messagebox.showinfo("Éxito", f"Libro con ID {book_id} actualizado.")
                self.clear_book_fields()
            except ValueError:
                messagebox.showerror("Error", "El ID, año de publicación y número de páginas deben ser números enteros.")
        else:
            messagebox.showerror("Error", "ID, título, año de publicación, editorial y número de páginas son obligatorios.")

    def delete_book(self):
        book_id_str = self.book_id_entry.get()
        if book_id_str:
            try:
                book_id = int(book_id_str)
                if messagebox.askyesno("Confirmar", f"¿Estás seguro de que quieres eliminar el libro con ID {book_id}?"):
                    db_functions.delete_book(book_id)
                    messagebox.showinfo("Éxito", f"Libro con ID {book_id} eliminado.")
                    self.clear_book_fields()
            except ValueError:
                messagebox.showerror("Error", "El ID del libro debe ser un número entero.")
        else:
            messagebox.showerror("Error", "Por favor, introduce el ID del libro a eliminar.")

    def clear_book_fields(self):
        self.book_id_entry.delete(0, tk.END)
        self.book_title_entry.delete(0, tk.END)
        self.book_isbn_entry.delete(0, tk.END)
        self.book_isbn13_entry.delete(0, tk.END)
        self.book_language_entry.delete(0, tk.END)
        self.book_publication_year_entry.delete(0, tk.END)
        self.book_publisher_entry.delete(0, tk.END)
        self.book_num_pages_entry.delete(0, tk.END)

    # ---------------------- TABLA AUTHORS ----------------------
    def create_authors_tab(self):
        self.authors_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.authors_tab, text='Autores')

        ttk.Label(self.authors_tab, text="Author ID:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.author_id_entry = ttk.Entry(self.authors_tab)
        self.author_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        ttk.Label(self.authors_tab, text="Nombre del Autor:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.author_name_entry = ttk.Entry(self.authors_tab)
        self.author_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        ttk.Button(self.authors_tab, text="Agregar Autor", command=self.add_author).grid(row=2, column=0, padx=5, pady=10, sticky='ew')
        ttk.Button(self.authors_tab, text="Obtener Autor", command=self.get_author).grid(row=2, column=1, padx=5, pady=10, sticky='ew')
        ttk.Button(self.authors_tab, text="Actualizar Autor", command=self.update_author).grid(row=3, column=0, padx=5, pady=10, sticky='ew')
        ttk.Button(self.authors_tab, text="Eliminar Autor", command=self.delete_author).grid(row=3, column=1, padx=5, pady=10, sticky='ew')

    def add_author(self):
        name = self.author_name_entry.get()
        if name:
            author = Author(author_name=name)
            db_functions.add_author(author=author)
            messagebox.showinfo("Éxito", f"Autor '{name}' agregado.")
            self.clear_author_fields()
        else:
            messagebox.showerror("Error", "El nombre del autor es obligatorio.")

    def get_author(self):
        author_id_str = self.author_id_entry.get()
        if author_id_str:
            try:
                author_id = int(author_id_str)
                author = db_functions.get_author(author_id)
                if author:
                    self.author_name_entry.delete(0, tk.END)
                    self.author_name_entry.insert(0, author.author_name)
                else:
                    messagebox.showinfo("Información", f"No se encontró ningún autor con ID {author_id}.")
            except ValueError:
                messagebox.showerror("Error", "El ID del autor debe ser un número entero.")
        else:
            messagebox.showerror("Error", "Por favor, introduce el ID del autor a buscar.")

    def update_author(self):
        author_id_str = self.author_id_entry.get()
        name = self.author_name_entry.get()
        if author_id_str and name:
            try:
                author_id = int(author_id_str)
                author = Author(authorid=author_id, author_name=name)
                db_functions.update_author(author=author)
                messagebox.showinfo("Éxito", f"Autor con ID {author_id} actualizado.")
                self.clear_author_fields()
            except ValueError:
                messagebox.showerror("Error", "El ID del autor debe ser un número entero.")
        else:
            messagebox.showerror("Error", "ID del autor y nombre son obligatorios.")

    def delete_author(self):
        author_id_str = self.author_id_entry.get()
        if author_id_str:
            try:
                author_id = int(author_id_str)
                if messagebox.askyesno("Confirmar", f"¿Estás seguro de que quieres eliminar el autor con ID {author_id}?"):
                    db_functions.delete_author(author_id)
                    messagebox.showinfo("Éxito", f"Autor con ID {author_id} eliminado.")
                    self.clear_author_fields()
            except ValueError:
                messagebox.showerror("Error", "El ID del autor debe ser un número entero.")
        else:
            messagebox.showerror("Error", "Por favor, introduce el ID del autor a eliminar.")

    def clear_author_fields(self):
        self.author_id_entry.delete(0, tk.END)
        self.author_name_entry.delete(0, tk.END)

    
    # ---------------------- TABLA GENRES ----------------------
    def create_genres_tab(self):
        self.genres_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.genres_tab, text='Géneros')

        ttk.Label(self.genres_tab, text="Genre ID:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.genre_id_entry = ttk.Entry(self.genres_tab)
        self.genre_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        ttk.Label(self.genres_tab, text="Nombre del Género:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.genre_name_entry = ttk.Entry(self.genres_tab)
        self.genre_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        ttk.Button(self.genres_tab, text="Agregar Género", command=self.add_genre).grid(row=2, column=0, padx=5, pady=10, sticky='ew')
        ttk.Button(self.genres_tab, text="Obtener Género", command=self.get_genre).grid(row=2, column=1, padx=5, pady=10, sticky='ew')
        ttk.Button(self.genres_tab, text="Actualizar Género", command=self.update_genre).grid(row=3, column=0, padx=5, pady=10, sticky='ew')
        ttk.Button(self.genres_tab, text="Eliminar Género", command=self.delete_genre).grid(row=3, column=1, padx=5, pady=10, sticky='ew')

    def add_genre(self): # <---- Método agregado
        name = self.genre_name_entry.get()
        if name:
            genre = Genre(genre_name=name)
            db_functions.add_genre(genre=genre)
            messagebox.showinfo("Éxito", f"Género '{name}' agregado.")
            self.clear_genre_fields()
        else:
            messagebox.showerror("Error", "El nombre del género es obligatorio.")

    def get_genre(self): # <---- Método agregado
        genre_id_str = self.genre_id_entry.get()
        if genre_id_str:
            try:
                genre_id = int(genre_id_str)
                genre = db_functions.get_genre(genre_id)
                if genre:
                    self.genre_name_entry.delete(0, tk.END)
                    self.genre_name_entry.insert(0, genre.genre_name)
                else:
                    messagebox.showinfo("Información", f"No se encontró ningún género con ID {genre_id}.")
            except ValueError:
                messagebox.showerror("Error", "El ID del género debe ser un número entero.")
        else:
            messagebox.showerror("Error", "Por favor, introduce el ID del género a buscar.")

    def update_genre(self): # <---- Método agregado
        genre_id_str = self.genre_id_entry.get()
        name = self.genre_name_entry.get()
        if genre_id_str and name:
            try:
                genre_id = int(genre_id_str)
                genre = Genre(genreid=genre_id, genre_name=name)
                db_functions.update_genre(genre=genre)
                messagebox.showinfo("Éxito", f"Género con ID {genre_id} actualizado.")
                self.clear_genre_fields()
            except ValueError:
                messagebox.showerror("Error", "El ID del género debe ser un número entero.")
        else:
            messagebox.showerror("Error", "ID del género y nombre son obligatorios.")

    def delete_genre(self): # <---- Método agregado
        genre_id_str = self.genre_id_entry.get()
        if genre_id_str:
            try:
                genre_id = int(genre_id_str)
                if messagebox.askyesno("Confirmar", f"¿Estás seguro de que quieres eliminar el género con ID {genre_id}?"):
                    db_functions.delete_genre(genre_id)
                    messagebox.showinfo("Éxito", f"Género con ID {genre_id} eliminado.")
                    self.clear_genre_fields()
            except ValueError:
                messagebox.showerror("Error", "El ID del género debe ser un número entero.")
        else:
            messagebox.showerror("Error", "Por favor, introduce el ID del género a eliminar.")

    def clear_genre_fields(self): # <---- Método agregado
        self.genre_id_entry.delete(0, tk.END)
        self.genre_name_entry.delete(0, tk.END)
if __name__ == '__main__':
    root = tk.Tk()
    app = GoodreadsApp(root)
    root.mainloop()