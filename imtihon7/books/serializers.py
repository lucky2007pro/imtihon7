from rest_framework import serializers
from .models import Section, Author, Book, BookReview, BookLike

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['id', 'name', 'created_time', 'updated_time']

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
        queryset=Section.objects.all(), source='section', write_only=True, allow_null=True, required=False
    )

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
