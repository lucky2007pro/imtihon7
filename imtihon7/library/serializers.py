from rest_framework import serializers
from .models import Reservation, Borrowing
from books.serializers import BookSerializer

class ReservationSerializer(serializers.ModelSerializer):
    book_details = BookSerializer(source='book', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    is_expired = serializers.BooleanField(read_only=True)

    class Meta:
        model = Reservation
        fields = [
            'id', 'user', 'user_name', 'book', 'book_details', 'status', 
            'expires_at', 'note', 'is_expired', 'created_time', 'updated_time'
        ]
        read_only_fields = ['user', 'expires_at', 'status']

    def validate(self, attrs):
        book = attrs.get('book')
        request = self.context.get('request')
        
        if request and request.user:
            user = request.user
            if Reservation.objects.filter(book=book, user=user, status='active').exists():
                raise serializers.ValidationError("Siz allaqachon bu kitobni band qilgansiz.")
                
        if Borrowing.objects.filter(book=book, is_returned=False).exists():
            raise serializers.ValidationError("Ushbu kitob ayni vaqtda boshqa kishida ijarada va uni band qilib bo'lmaydi.")
            
        return attrs

class BorrowingSerializer(serializers.ModelSerializer):
    book_details = BookSerializer(source='book', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Borrowing
        fields = [
            'id', 'user', 'user_name', 'book', 'book_details', 'return_date', 
            'is_returned', 'returned_date', 'created_time', 'updated_time'
        ]
        read_only_fields = ['user', 'is_returned', 'returned_date']

    def validate(self, attrs):
        book = attrs.get('book')
        
        if self.instance is None and Borrowing.objects.filter(book=book, is_returned=False).exists():
            raise serializers.ValidationError("Bu kitob allaqachon boshqaga ijaraga berilgan va qaytarilmagan.")
            
        return attrs
