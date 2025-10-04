from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Author, Book

class BookAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(
            title="Test Book",
            publication_year=2020,
            author=self.author
        )
        self.client = APIClient()
        self.book_list_url = reverse('book-list')
        self.book_detail_url = reverse('book-detail', args=[self.book.id])
        self.book_create_url = reverse('book-create')
        self.book_update_url = reverse('book-update', args=[self.book.id])
        self.book_delete_url = reverse('book-delete', args=[self.book.id])

    def test_book_list(self):
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_book_detail(self):
        response = self.client.get(self.book_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Test Book")

    def test_book_create_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        data = {
            'title': 'New Book',
            'publication_year': 2022,
            'author': self.author.id
        }
        response = self.client.post(self.book_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_book_create_unauthenticated(self):
        data = {
            'title': 'Unauthorized Book',
            'publication_year': 2023,
            'author': self.author.id
        }
        response = self.client.post(self.book_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_book_update(self):
        self.client.login(username='testuser', password='testpass')
        data = {
            'title': 'Updated Book',
            'publication_year': 2021,
            'author': self.author.id
        }
        response = self.client.put(self.book_update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Book')

    def test_book_delete(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.delete(self.book_delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())

    def test_filtering_books_by_year(self):
        response = self.client.get(f"{self.book_list_url}?publication_year=2020")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_books_by_title(self):
        response = self.client.get(f"{self.book_list_url}?search=Test")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_ordering_books_by_year(self):
        Book.objects.create(title="Another Book", publication_year=2019, author=self.author)
        response = self.client.get(f"{self.book_list_url}?ordering=publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLessEqual(response.data[0]['publication_year'], response.data[1]['publication_year'])
