from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SectionViewSet, AuthorViewSet, BookViewSet, BookReviewViewSet, BookLikeViewSet

router = DefaultRouter()
router.register(r'sections', SectionViewSet)
router.register(r'authors', AuthorViewSet)
router.register(r'books', BookViewSet)
router.register(r'reviews', BookReviewViewSet, basename='bookreview')
router.register(r'likes', BookLikeViewSet, basename='booklike')

urlpatterns = [
    path('', include(router.urls)),
]
