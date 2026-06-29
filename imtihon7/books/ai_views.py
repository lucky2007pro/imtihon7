import os
from google import genai
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework import serializers
from drf_spectacular.utils import extend_schema

class AIRequestSerializer(serializers.Serializer):
    prompt = serializers.CharField(required=True, help_text="Savolingizni kiriting")

class AIResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    response = serializers.CharField()

class AIAssistantView(APIView):
    permission_classes = [AllowAny]
    serializer_class = AIRequestSerializer

    @extend_schema(
        request=AIRequestSerializer,
        responses={200: AIResponseSerializer}
    )
    def post(self, request):
        serializer = AIRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        prompt = serializer.validated_data['prompt']
        from django.conf import settings
        
        api_key = getattr(settings, 'GEMINI_API_KEY', None)
        if api_key:
            api_key = api_key.strip()
            print("USING API KEY STARTING WITH:", api_key[:15])
        model_name = getattr(settings, 'GEMINI_MODEL', 'gemini-2.5-flash')
        
        if not api_key:
            return Response({
                "success": False,
                "response": "Sun'iy intellekt xizmati sozlanmagan (GEMINI_API_KEY topilmadi)."
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            
        try:
            client = genai.Client(api_key=api_key)
            
            # Simple prompt augmentation
            full_prompt = f"Sen kutubxona tizimi uchun maslahatchisan. Quyidagi savolga javob ber: {prompt}"
            
            response = client.models.generate_content(
                model=model_name,
                contents=full_prompt,
            )
            
            return Response({
                "success": True,
                "response": response.text
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({
                "success": False,
                "response": f"Xatolik yuz berdi: {str(e)} (API KEY USED: {api_key[:15]}...)"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
