from rest_framework import viewsets, status, mixins
from .models import User
from .serializers import UserSerializer, RegisterUserSerializer, LoginSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema


class RegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer
    permission_classes = [AllowAny]


class LoginViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    @swagger_auto_schema(request_body=LoginSerializer)

    def create(self, request, *args, **kwargs):
        """
        Handle user login (POST request)
        """
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            # Valid login, returning access and refresh tokens
            user = serializer.validated_data['user']
            user_data = UserSerializer(user).data
            return Response({
                'refresh': serializer.validated_data['refresh'],
                'access': serializer.validated_data['access'],
                'user': user_data
            }, status=status.HTTP_200_OK)

        # If invalid login credentials
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)