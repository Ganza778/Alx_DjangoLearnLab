import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian


author_name = "J.K. Rowling"
try:
    author = Author.objects.get(name=author_name)

    books_by_author = Book.objects.filter(author=author)
    print(f"Books by {author_name}: {[book.title for book in books_by_author]}")
except Author.DoesNotExist:
    print(f"No author found with the name {author_name}")


library_name = "Central Library"
try:
    library = Library.objects.get(name=library_name)

    books_in_library = library.books.all()
    print(f"Books in {library_name}: {[book.title for book in books_in_library]}")
except Library.DoesNotExist:
    print(f"No library found with the name {library_name}")


try:
    librarian = Librarian.objects.get(library=library)
    print(f"Librarian of {library_name}: {librarian.name}")
except Librarian.DoesNotExist:
    print(f"No librarian assigned to {library_name}")
