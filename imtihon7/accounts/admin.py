from django.contrib import admin
from .models import CustomUser, CodeVerify

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'user_role', 'is_approved']
    list_filter = ['user_role', 'is_approved']
    search_fields = ['email', 'username', 'phone_number', 'first_name', 'last_name']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(CodeVerify)