from shared.custom_responses import CustomModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Reservation, Borrowing
from .serializers import ReservationSerializer, BorrowingSerializer
from books.permissions import IsAdmin

class ReservationViewSet(CustomModelViewSet):
    queryset = Reservation.objects.all().select_related('user', 'book')
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff and getattr(self.request.user, 'user_role', '') != 'admin':
            qs = qs.filter(user=self.request.user)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BorrowingViewSet(CustomModelViewSet):
    queryset = Borrowing.objects.all().select_related('user', 'book')
    serializer_class = BorrowingSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return [IsAuthenticated()]

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff and getattr(self.request.user, 'user_role', '') != 'admin':
            qs = qs.filter(user=self.request.user)
        return qs
