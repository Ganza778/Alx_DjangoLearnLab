# delete.md

>>> from bookshelf.models import Book
>>> book.delete()
# (1, {'bookshelf.Book': 1})  ← Confirmation of deletion

>>> Book.objects.all()
# <QuerySet []>  ← Empty list confirms deletion
