from django.shortcuts import render

from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer


class BookListView(generics.ListAPIView):
    """
    GET /books/
    List all books.
    Open to all users (read-only).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


class BookDetailView(generics.RetrieveAPIView):
    """
    GET /books/<int:pk>/
    Retrieve a single book by ID.
    Open to all users (read-only).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


class BookCreateView(generics.CreateAPIView):
    """
    POST /books/
    Create a new book.
    Only authenticated users allowed.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookUpdateView(generics.UpdateAPIView):
    """
    PUT/PATCH /books/<int:pk>/
    Update an existing book.
    Only authenticated users allowed.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookDeleteView(generics.DestroyAPIView):
    """
    DELETE /books/<int:pk>/
    Delete a book.
    Only authenticated users allowed.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

