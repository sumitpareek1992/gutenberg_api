from django.db import models

# Create your models here.
class Language(models.Model):
    code = models.CharField(max_length=4, unique=True)

    def __str__(self):
        return self.code
    
    class Meta:
        managed = False 
        db_table = "books_language"

class Author(models.Model):
    birth_year = models.PositiveIntegerField(blank=True, null=True)
    death_year = models.PositiveIntegerField(blank=True, null=True)
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name
    
    class Meta:
        managed = False 
        db_table = "books_author"
    
class Subject(models.Model):
    name = models.CharField(max_length=256)
    def __str__(self):
        return self.name
    class Meta:
        managed = False 
        db_table = "books_subject"

class Bookshelf(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name
    class Meta:
        managed = False 
        db_table = "books_bookshelf"

class Book(models.Model):
    authors = models.ManyToManyField(Author)
    bookshelves = models.ManyToManyField(Bookshelf)
    download_count = models.PositiveIntegerField(blank=True, null=True)
    gutenberg_id = models.PositiveIntegerField(unique=True)
    languages = models.ManyToManyField(Language)
    subjects = models.ManyToManyField(Subject)
    title = models.CharField(blank=True, max_length=1024, null=True)

    def __str__(self):
        if self.title:
            return self.title
        else:
            return str(self.id)
    def get_formats(self):
        return Format.objects.filter(book_id=self.id)
    
    class Meta:
        managed = False 
        db_table = "books_book"



class Format(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE,related_name='format')
    mime_type = models.CharField(max_length=32)
    url = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.mime_type} ({self.book.__str__()})"
    class Meta:
        managed = False 
        db_table = "books_format"











class Summary(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        preview_len = 24
        return f'{self.text[:preview_len]}...' if len(self.text) > preview_len else self.text
