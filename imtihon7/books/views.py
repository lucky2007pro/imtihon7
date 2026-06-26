from rest_framework import filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from shared.custom_responses import CustomModelViewSet
from .models import Section, Author, Book, BookReview, BookLike
from .serializers import (
    SectionSerializer, AuthorSerializer, BookSerializer, 
    BookReviewSerializer, BookLikeSerializer
)
from .permissions import IsAdminOrReadOnly

class SectionViewSet(CustomModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class AuthorViewSet(CustomModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name']

class BookViewSet(CustomModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'isbn', 'author__first_name', 'author__last_name']
    ordering_fields = ['title', 'view_count', 'published_date']
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.view_count += 1
        instance.save(update_fields=['view_count'])
        return super().retrieve(request, *args, **kwargs)

class BookReviewViewSet(CustomModelViewSet):
    queryset = BookReview.objects.all().select_related('user', 'book')
    serializer_class = BookReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        qs = super().get_queryset()
        book_id = self.request.query_params.get('book')
        if book_id:
            qs = qs.filter(book_id=book_id)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BookLikeViewSet(CustomModelViewSet):
    queryset = BookLike.objects.all().select_related('user', 'book')
    serializer_class = BookLikeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        qs = super().get_queryset()
        book_id = self.request.query_params.get('book')
        if book_id:
            qs = qs.filter(book_id=book_id)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
