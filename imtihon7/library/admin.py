from django.contrib import admin
from .models import Reservation, Borrowing

admin.site.register(Reservation)
admin.site.register(Borrowing)
