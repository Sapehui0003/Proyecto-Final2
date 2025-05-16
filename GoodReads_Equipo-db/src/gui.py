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
        self.create_reviews_tab()
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

    # ---------------------- TABLA REVIEWS ----------------------
    def create_reviews_tab(self):
        self.reviews_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.reviews_tab, text='Reseñas')

        # Campos para agregar/actualizar reseña
        ttk.Label(self.reviews_tab, text="Review ID:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.review_id_entry = ttk.Entry(self.reviews_tab)
        self.review_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        ttk.Label(self.reviews_tab, text="User ID:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.user_id_entry = ttk.Entry(self.reviews_tab)
        self.user_id_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        ttk.Label(self.reviews_tab, text="Book ID:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.book_id_entry_review = ttk.Entry(self.reviews_tab)  # Changed variable name to avoid conflict
        self.book_id_entry_review.grid(row=2, column=1, padx=5, pady=5, sticky='ew')

        ttk.Label(self.reviews_tab, text="Rating:").grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.rating_entry = ttk.Entry(self.reviews_tab)
        self.rating_entry.grid(row=3, column=1, padx=5, pady=5, sticky='ew')

        ttk.Label(self.reviews_tab, text="Review Text:").grid(row=4, column=0, padx=5, pady=5, sticky='w')
        self.review_text_entry = ttk.Entry(self.reviews_tab)
        self.review_text_entry.grid(row=4, column=1, padx=5, pady=5, sticky='ew')

        ttk.Label(self.reviews_tab, text="Review Date:").grid(row=5, column=0, padx=5, pady=5, sticky='w')
        self.review_date_entry = ttk.Entry(self.reviews_tab)
        self.review_date_entry.grid(row=5, column=1, padx=5, pady=5, sticky='ew')

        # Botones para operaciones de reseñas
        ttk.Button(self.reviews_tab, text="Agregar Reseña", command=self.add_review).grid(row=6, column=0, padx=5, pady=10, sticky='ew')
        ttk.Button(self.reviews_tab, text="Obtener Reseña", command=self.get_review).grid(row=6, column=1, padx=5, pady=10, sticky='ew')
        ttk.Button(self.reviews_tab, text="Actualizar Reseña", command=self.update_review).grid(row=7, column=0, padx=5, pady=10, sticky='ew')
        ttk.Button(self.reviews_tab, text="Eliminar Reseña", command=self.delete_review).grid(row=7, column=1, padx=5, pady=10, sticky='ew')
        ttk.Button(self.reviews_tab, text="Obtener Todas las Reseñas", command=self.get_all_reviews).grid(row=8, column=0, padx=5, pady=10, sticky='ew')

    def add_review(self):
        review_id = self.review_id_entry.get()
        user_id = self.user_id_entry.get()
        book_id_str = self.book_id_entry_review.get() # Changed variable name
        rating_str = self.rating_entry.get()
        review_text = self.review_text_entry.get()
        review_date = self.review_date_entry.get()

        if review_id and user_id and book_id_str and rating_str:
            try:
                book_id = int(book_id_str)
                rating = int(rating_str)
                if 0 <= rating <= 5:
                    review = Review(
                        reviewid=review_id,
                        userid=user_id,
                        bookid=book_id,
                        rating=rating,
                        reviewtext=review_text,
                        reviewdate=review_date
                    )
                    db_functions.add_review(review=review)
                    messagebox.showinfo("Éxito", f"Reseña con ID '{review_id}' agregada.")
                    self.clear_review_fields()
                else:
                    messagebox.showerror("Error", "La calificación (rating) debe estar entre 0 y 5.")
            except ValueError:
                messagebox.showerror("Error", "El Book ID y la calificación (rating) deben ser números enteros.")
        else:
            messagebox.showerror("Error", "Review ID, User ID, Book ID y calificación son obligatorios.")

    def get_review(self):
        review_id = self.review_id_entry.get()
        if review_id:
            review = db_functions.get_review(review_id) # Assuming you have this function in db_functions
            if review:
                self.user_id_entry.delete(0, tk.END)
                self.user_id_entry.insert(0, review.userid)
                self.book_id_entry_review.delete(0, tk.END) # Changed variable name
                self.book_id_entry_review.insert(0, review.bookid)
                self.rating_entry.delete(0, tk.END)
                self.rating_entry.insert(0, review.rating)
                self.review_text_entry.delete(0, tk.END)
                self.review_text_entry.insert(0, review.reviewtext)
                self.review_date_entry.delete(0, tk.END)
                self.review_date_entry.insert(0, review.reviewdate)
            else:
                messagebox.showinfo("Información", f"No se encontró ninguna reseña con ID {review_id}.")
        else:
            messagebox.showerror("Error", "Por favor, introduce el ID de la reseña a buscar.")

    def update_review(self):
        review_id = self.review_id_entry.get()
        user_id = self.user_id_entry.get()
        book_id_str = self.book_id_entry_review.get()  # Changed variable name
        rating_str = self.rating_entry.get()
        review_text = self.review_text_entry.get()
        review_date = self.review_date_entry.get()
        
        if review_id and user_id and book_id_str: #made book_id_str a requirement
            try:
                book_id = int(book_id_str)
                rating = int(rating_str) if rating_str else None #make rating optional
                
                if rating is None or (0 <= rating <= 5): #check if rating is None
                    db_functions.update_review(review_id, rating, review_text, review_date)
                    messagebox.showinfo("Éxito", f"Reseña con ID {review_id} actualizada.")
                    self.clear_review_fields()
                else:
                    messagebox.showerror("Error", "La calificación debe estar entre 0 y 5.")
            except ValueError:
                messagebox.showerror("Error", "Book ID y la calificación deben ser números enteros.")
        else:
            messagebox.showerror("Error", "Review ID, User ID and Book ID son obligatorios.")

    def delete_review(self):
        review_id = self.review_id_entry.get()
        if review_id:
            if messagebox.askyesno("Confirmar", f"¿Estás seguro de que quieres eliminar la reseña con ID {review_id}?"):
                db_functions.delete_review(review_id)
                messagebox.showinfo("Éxito", f"Reseña con ID {review_id} eliminada.")
                self.clear_review_fields()
        else:
            messagebox.showerror("Error", "Por favor, introduce el ID de la reseña a eliminar.")

    def clear_review_fields(self):
        self.review_id_entry.delete(0, tk.END)
        self.user_id_entry.delete(0, tk.END)
        self.book_id_entry_review.delete(0, tk.END) # Changed variable name
        self.rating_entry.delete(0, tk.END)
        self.review_text_entry.delete(0, tk.END)
        self.review_date_entry.delete(0, tk.END)
        
    def get_all_reviews(self):
        reviews = db_functions.get_all_reviews()
        if reviews:
            # Create a new window to display the reviews
            reviews_window = tk.Toplevel(self.master)
            reviews_window.title("Todas las Reseñas")

            # Create a treeview widget to display the reviews in a table format
            tree = ttk.Treeview(reviews_window, cols=("Review ID", "User ID", "Book ID", "Rating", "Review Text", "Review Date"), show="headings")
            tree.heading("Review ID", text="Review ID")
            tree.heading("User ID", text="User ID")
            tree.heading("Book ID", text="Book ID")
            tree.heading("Rating", text="Rating")
            tree.heading("Review Text", text="Review Text")
            tree.heading("Review Date", text="Review Date")
            tree.pack(expand=True, fill='both')

            # Insert the reviews into the treeview
            for review in reviews:
                tree.insert("", tk.END, values=(review["reviewid"], review["userid"], review["bookid"], review["rating"], review["reviewtext"], review["reviewdate"]))
        else:
            messagebox.showinfo("Información", "No hay reseñas para mostrar.")

if __name__ == '__main__':
    root = tk.Tk()
    app = GoodreadsApp(root)
    root.mainloop()