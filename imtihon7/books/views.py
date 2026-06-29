from rest_framework import filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from shared.custom_responses import CustomModelViewSet
from .permissions import IsAdminOrReadOnly, IsAdminOrLibrarian
import math
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from django.db import models
from .models import Section, Author, Book, BookReview, BookLike, LibraryBook
from .serializers import (
    SectionSerializer, AuthorSerializer, BookSerializer, 
    BookReviewSerializer, BookLikeSerializer, NearestLibrarySerializer,
    LibraryBookSerializer
)

class SectionViewSet(CustomModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [IsAdminOrLibrarian]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        # Librarian faqat o'z bo'limlarini ko'radi
        if user.is_authenticated and getattr(user, 'user_role', '') == 'librarian':
            return qs.filter(library=user)
        return qs

    def perform_create(self, serializer):
        user = self.request.user
        # Librarian yaratganda avtomatik o'ziga bog'lanadi
        if user.is_authenticated and getattr(user, 'user_role', '') == 'librarian':
            serializer.save(library=user)
        else:
            serializer.save()

class AuthorViewSet(CustomModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminOrLibrarian]
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name']

class BookViewSet(CustomModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrLibrarian]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'isbn', 'author__first_name', 'author__last_name']
    ordering_fields = ['title', 'view_count', 'published_date']
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.view_count += 1
        instance.save(update_fields=['view_count'])
        return super().retrieve(request, *args, **kwargs)

    def perform_create(self, serializer):
        book = serializer.save()
        user = self.request.user
        if user.is_authenticated and user.user_role == 'librarian':
            LibraryBook.objects.create(
                library=user,
                book=book,
                available_copies=book.total_copies
            )

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

class LibraryBookViewSet(CustomModelViewSet):
    queryset = LibraryBook.objects.all().select_related('library', 'book')
    serializer_class = LibraryBookSerializer
    permission_classes = [IsAdminOrLibrarian]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_authenticated and self.request.user.user_role == 'librarian':
            return qs.filter(library=self.request.user)
        return qs

    def perform_create(self, serializer):
        serializer.save(library=self.request.user)

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

def haversine(lat1, lon1, lat2, lon2):
    if lat1 is None or lon1 is None or lat2 is None or lon2 is None:
        return float('inf')
    R = 6371.0
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    return R * c

class SearchNearestLibraryView(APIView):
    permission_classes = [AllowAny]
    
    @extend_schema(
        parameters=[
            OpenApiParameter('q', OpenApiTypes.STR, description="Kitob nomi yoki muallifi", required=True),
            OpenApiParameter('lat', OpenApiTypes.FLOAT, description="Foydalanuvchi kengligi (latitude)", required=True),
            OpenApiParameter('lng', OpenApiTypes.FLOAT, description="Foydalanuvchi uzunligi (longitude)", required=True),
        ],
        responses=NearestLibrarySerializer(many=True)
    )
    def get(self, request):
        q = request.query_params.get('q', '')
        try:
            user_lat = float(request.query_params.get('lat'))
            user_lng = float(request.query_params.get('lng'))
        except (TypeError, ValueError):
            return Response({"xatolik": "lat va lng parametrlarini to'g'ri kiriting."}, status=400)
            
        if not q:
            return Response({"xatolik": "q parametrini (kitob qidiruv so'zini) kiriting."}, status=400)

        library_books = LibraryBook.objects.filter(
            available_copies__gt=0
        ).filter(
            models.Q(book__title__icontains=q) |
            models.Q(book__author__first_name__icontains=q) |
            models.Q(book__author__last_name__icontains=q)
        ).select_related('library', 'book')

        results = []
        for lb in library_books:
            lib = lb.library
            distance = haversine(user_lat, user_lng, lib.library_lat, lib.library_lng)
            results.append({
                'book_id': lb.book.id,
                'book_title': lb.book.title,
                'cover_image': lb.book.cover_image.url if lb.book.cover_image else None,
                'library_name': lib.library_name or lib.username,
                'library_location': lib.library_location or "",
                'distance_km': round(distance, 2),
                'available_copies': lb.available_copies,
            })
            
        results.sort(key=lambda x: x['distance_km'])
        
        serializer = NearestLibrarySerializer(results, many=True)
        return Response(serializer.data)
