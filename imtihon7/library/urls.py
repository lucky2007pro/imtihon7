from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReservationViewSet, BorrowingViewSet

router = DefaultRouter()
router.register(r'reservations', ReservationViewSet, basename='reservation')
router.register(r'borrowings', BorrowingViewSet, basename='borrowing')

urlpatterns = [
    path('', include(router.urls)),
]
