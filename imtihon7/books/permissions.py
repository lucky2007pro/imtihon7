from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):

    message = 'Admin ruxsati talab qilinadi.'

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return bool(
            request.user and 
            request.user.is_authenticated and 
            (request.user.is_staff or request.user.is_superuser or getattr(request.user, 'user_role', '') == 'admin')
        )


class IsAdmin(BasePermission):

    message = 'Ushbu amalni bajarish uchun Admin bo\'lishingiz kerak.'

    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            (request.user.is_staff or request.user.is_superuser or getattr(request.user, 'user_role', '') == 'admin')
        )


class IsAdminOrLibrarian(BasePermission):

    message = 'Bu amalni bajarish uchun Admin yoki Librarian bo\'lishingiz kerak.'

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if not request.user or not request.user.is_authenticated:
            return False

        user_role = getattr(request.user, 'user_role', '')
        return bool(
            request.user.is_staff or
            request.user.is_superuser or
            user_role == 'admin' or
            user_role == 'librarian'
        )

