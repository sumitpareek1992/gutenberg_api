# serializers.py
from rest_framework import serializers
from books_store.models import Book, Author, Language, Subject, Bookshelf, Format

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name', 'birth_year', 'death_year']

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['code']

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['name']

class BookshelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookshelf
        fields = ['name']

class FormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Format
        fields = ['mime_type', 'url']

class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)
    languages = LanguageSerializer(many=True)
    subjects = SubjectSerializer(many=True)
    bookshelves = BookshelfSerializer(many=True)
    formats = serializers.SerializerMethodField()
    book_id = serializers.IntegerField(source='gutenberg_id')

    class Meta:
        model = Book
        fields = ['title', 'authors', 'languages', 'subjects', 'bookshelves', 'formats','book_id']

    def get_formats(self, obj):
        return FormatSerializer(obj.get_formats(), many=True).data
