from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

def custom_response(success, message, data=None, status_code=status.HTTP_200_OK):
    return Response({
        'success': success,
        'message': message,
        'data': data
    }, status=status_code)

class CustomModelViewSet(ModelViewSet):

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        if 'results' in response.data or 'success' in response.data:
            return response
        return custom_response(True, "Ma'lumotlar ro'yxati olindi.", response.data)

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return custom_response(True, "Ma'lumot muvaffaqiyatli olindi.", response.data)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return custom_response(True, "Muvaffaqiyatli saqlandi.", response.data, status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return custom_response(True, "Muvaffaqiyatli yangilandi.", response.data)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return custom_response(True, "Muvaffaqiyatli o'chirildi.", status_code=status.HTTP_204_NO_CONTENT)
