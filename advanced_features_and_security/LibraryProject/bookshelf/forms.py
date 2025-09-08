# LibraryProject/bookshelf/forms.py
from django import forms
from .models import Book


class ExampleForm(forms.ModelForm):
    """Secure form for creating or editing Book objects.
    Uses Django's form validation to prevent SQL injection and XSS.
    """

    class Meta:
        model = Book
        fields = ["title", "author"]

    def clean_title(self):
        title = self.cleaned_data.get("title")
        # Extra sanitization or validation logic can go here
        return title
