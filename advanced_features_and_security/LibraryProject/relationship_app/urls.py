from django.urls import path
from .views import list_books, LibraryDetailView, add_book, edit_book, delete_book
from .views import register_view, admin_view, librarian_view, member_view
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('list_books/', list_books, name='list_books'),

    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    path('add_book/', add_book, name='add_book'),
    path('edit_book/<int:book_id>/', edit_book, name='edit_book'),
    path('delete_book/<int:book_id>/', delete_book, name='delete_book'),

    path('register/', views.register, name='register'), 
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),

    path('admin/', admin_view, name='admin_view'),
    path('librarian/', librarian_view, name='librarian_view'),
    path('member/', member_view, name='member_view'),
]
