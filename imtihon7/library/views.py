from shared.custom_responses import CustomModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Reservation, Borrowing
from .serializers import ReservationSerializer, BorrowingSerializer
from books.permissions import IsAdmin, IsAdminOrLibrarian

class ReservationViewSet(CustomModelViewSet):
    queryset = Reservation.objects.all().select_related('user', 'book', 'library')
    serializer_class = ReservationSerializer
    
    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            return [IsAdminOrLibrarian()]
        return [IsAuthenticated()]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if not user.is_staff and getattr(user, 'user_role', '') != 'admin':
            if getattr(user, 'user_role', '') == 'librarian':
                qs = qs.filter(library=user)
            else:
                qs = qs.filter(user=user)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BorrowingViewSet(CustomModelViewSet):
    queryset = Borrowing.objects.all().select_related('user', 'book', 'library')
    serializer_class = BorrowingSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminOrLibrarian()]
        return [IsAuthenticated()]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if not user.is_staff and getattr(user, 'user_role', '') != 'admin':
            if getattr(user, 'user_role', '') == 'librarian':
                qs = qs.filter(library=user)
            else:
                qs = qs.filter(user=user)
        return qs

    def perform_create(self, serializer):
        user = self.request.user
        if getattr(user, 'user_role', '') == 'librarian':
            serializer.save(library=user)
        else:
            serializer.save()
