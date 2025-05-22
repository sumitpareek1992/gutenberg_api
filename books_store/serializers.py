# serializers.py
from rest_framework import serializers
from books_store.models import Book, Author, Language, Subject, Bookshelf, Format
GENRE_MAP = {
    "Science fiction": "Science Fiction",
    "Children": "Children",
    "Historical": "Historical Fiction",
    "Romance": "Romance",
    "Mystery": "Mystery",
    "Fantasy": "Fantasy",
    "Adventure": "Adventure",
    "Poetry": "Poetry"
}
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
    genre = serializers.SerializerMethodField()


    class Meta:
        model = Book
        fields = ['title','genre', 'authors', 'languages', 'subjects', 'bookshelves', 'formats','book_id']

    def get_formats(self, obj):
        return FormatSerializer(obj.get_formats(), many=True).data
    def get_genre(self, obj):
        keywords = list(obj.bookshelves.values_list('name', flat=True)) + list(obj.subjects.values_list('name', flat=True))
        for keyword in keywords:
            for key, genre in GENRE_MAP.items():
                if key.lower() in keyword.lower():
                    return genre
        return "Unknown"
