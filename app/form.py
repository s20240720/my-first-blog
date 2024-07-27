from django.forms import ModelForm
from app.models import Book, Author, Log

class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ('name',)

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'read_date', 'author', 'isbn')

class LogForm(ModelForm):
    class Meta:
        model = Log
        fields = ('book', 'text')
