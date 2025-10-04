from django.db import models

class Author(models.Model):
    """
    The Author model represents a writer in the system.
    Each author can have multiple books — this is a one-to-many relationship.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    The Book model represents a book written by an author.
    It includes the title, publication year, and a foreign key to the author.
    The ForeignKey creates a many-to-one relationship (many books to one author).
    """
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books'  # Allows reverse access: author.books
    )

    def __str__(self):
        return self.title
