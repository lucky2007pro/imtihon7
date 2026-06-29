from rest_framework import serializers
from .models import Section, Author, Book, BookReview, BookLike, LibraryBook

class SectionSerializer(serializers.ModelSerializer):
    library_name = serializers.CharField(source='library.library_name', read_only=True, allow_null=True)

    class Meta:
        model = Section
        fields = ['id', 'name', 'library', 'library_name', 'created_time', 'updated_time']
        read_only_fields = ['library']

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name', 'bio', 'created_time', 'updated_time']

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), source='author', write_only=True, allow_null=True, required=False
    )
    section = SectionSerializer(read_only=True)
    section_id = serializers.PrimaryKeyRelatedField(
        queryset=Section.objects.none(), source='section', write_only=True, allow_null=True, required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user = request.user
            user_role = getattr(user, 'user_role', '')
            if user_role == 'librarian':
                # Librarian faqat o'z bo'limlarini tanlaydi
                self.fields['section_id'].queryset = Section.objects.filter(library=user)
            else:
                # Admin barcha bo'limlarni ko'radi
                self.fields['section_id'].queryset = Section.objects.all()
        else:
            self.fields['section_id'].queryset = Section.objects.all()

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'author_id', 'section', 'section_id', 
            'description', 'published_date', 'isbn', 'cover_image', 
            'pdf_file', 'total_copies', 'view_count', 'created_time', 'updated_time'
        ]


class BookReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = BookReview
        fields = ['id', 'user', 'user_name', 'book', 'rating', 'comment', 'created_time']
        read_only_fields = ['user']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating kamida 1, ko'pi bilan 5 bo'lishi kerak.")
        return value

class BookLikeSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = BookLike
        fields = ['id', 'user', 'user_name', 'book', 'created_time']
        read_only_fields = ['user']

class LibraryBookSerializer(serializers.ModelSerializer):
    library_name = serializers.CharField(source='library.library_name', read_only=True)
    library_location = serializers.CharField(source='library.library_location', read_only=True)
    book_title = serializers.CharField(source='book.title', read_only=True)

    class Meta:
        model = LibraryBook
        fields = ['id', 'library', 'library_name', 'library_location', 'book', 'book_title', 'available_copies']
        read_only_fields = ['library']

class NearestLibrarySerializer(serializers.Serializer):
    book_id = serializers.IntegerField()
    book_title = serializers.CharField()
    cover_image = serializers.CharField(allow_null=True)
    library_name = serializers.CharField()
    library_location = serializers.CharField()
    distance_km = serializers.FloatField()
    available_copies = serializers.IntegerField()
