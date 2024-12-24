from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
import secrets

from auth_service import settings
from .models import PasswordResetToken
from .serializer import *
User = get_user_model()

import logging
logger = logging.getLogger(__name__)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

            refresh = RefreshToken.for_user(user)

            return Response({
                "user": UserSerializer(user).data,
                "message": "Usuario creado exitosamente",
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            # Detalles del error de validación
            return Response({
                "error": e.get_full_details()  # Esto te dará detalles más específicos sobre el error
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Si ocurre otro tipo de excepción
            return Response({
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"message": "Logout exitoso"},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": "Token inválido"},
                status=status.HTTP_400_BAD_REQUEST
            )

class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)

            # Generar token único
            token = secrets.token_urlsafe(32)
            PasswordResetToken.objects.create(
                user=user,
                token=token
            )

            # Enviar email
            reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"
            return Response({
                "message": "Enlace de restablecimiento generado exitosamente.",
                "reset_url": reset_url
            })
        except User.DoesNotExist:
            # Misma respuesta para evitar revelar si el email existe
            return Response({
                "message": "Si el correo existe en nuestra base de datos, recibirás instrucciones para recuperar tu contraseña"
            })


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            reset_token = PasswordResetToken.objects.get(
                token=serializer.validated_data['token'],
                is_used=False
            )

            if not reset_token.is_valid():
                return Response(
                    {"error": "El token ha expirado"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Cambiar contraseña
            user = reset_token.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()

            # Marcar token como usado
            reset_token.is_used = True
            reset_token.save()

            return Response({"message": "Contraseña actualizada exitosamente"})

        except PasswordResetToken.DoesNotExist:
            return Response(
                {"error": "Token inválido"},
                status=status.HTTP_400_BAD_REQUEST
            )
