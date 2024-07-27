from django.db import models
from django.utils import timezone

class Author(models.Model):
    name = models.CharField(max_length=100, verbose_name="著者")
    def __str__(self):
        return self.name
    
class Book(models.Model):
    title = models.CharField(max_length=100, verbose_name="タイトル")
    read_date = models.DateField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="著者", related_name='book')
    isbn = models.CharField(max_length=13, verbose_name="ISBN", default="00000000000000")
    def __str__(self):
        return self.title
    
class Log(models.Model):
    text = models.TextField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="タイトル", related_name='log')
    def __str__(self):
        return self.text

