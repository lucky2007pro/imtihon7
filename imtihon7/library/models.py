from datetime import timedelta
from django.db import models
from django.utils import timezone
from django.conf import settings
from shared.models import BaseModel
from books.models import Book

def _default_reservation_expiry():
    """Bron sukut bo'yicha yaratilgandan 3 kun keyin tugaydi."""
    return timezone.now() + timedelta(days=3)

class Reservation(BaseModel):
    STATUS_CHOICES = (
        ('pending', 'Kutilmoqda'),
        ('active', 'Tasdiqlangan'),
        ('cancelled', 'Bekor qilingan'),
        ('completed', 'Yakunlangan'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservations')
    library = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='library_reservations',
        limit_choices_to={'user_role': 'librarian'}, null=True, blank=True
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reservations')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    expires_at = models.DateTimeField(default=_default_reservation_expiry)
    note = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} reserved {self.book.title} ({self.status})"

    @property
    def is_expired(self):
        return self.expires_at is not None and self.expires_at <= timezone.now()

class Borrowing(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='borrowings')
    library = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='library_borrowings',
        limit_choices_to={'user_role': 'librarian'}, null=True, blank=True
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrowings')
    return_date = models.DateField()
    is_returned = models.BooleanField(default=False)
    returned_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title}"