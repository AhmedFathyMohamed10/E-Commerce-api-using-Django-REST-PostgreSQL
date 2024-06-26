from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.permissions import AllowAny
# ------------------------------------------------------------
from rest_framework.views import exception_handler
# ------------------------------------------------------------

from .serializers import UserSerializer, AuthTokenSerializer

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'Failed': 'Your are not logged in user!'}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        if user.is_authenticated:
            user.auth_token.delete()
            return Response({'Logged Out': 'You are now logged out.'}, status=status.HTTP_200_OK)
        return Response({'error': 'User not authenticated'}, status=status.HTTP_400_BAD_REQUEST)


def custom_404_view(request, exception):
    return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)