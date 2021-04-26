from users.models import User, Token

from .serializers import (UserSerializer, TokenSerializer)
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers


from django.db import transaction

from utils.helpers import send_mail
from users.services.token import TokenService


class UserLoginViewJWT(jwt_views.TokenObtainPairView):
    user_serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            user = User.objects.get(email=request.data[User.USERNAME_FIELD])
            serialized_user = self.user_serializer_class(user)
            response.data["data"] = {
                "user": serialized_user.data}

        return response


class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        token_service = TokenService()
        token, expires_at = token_service.generate_token(seconds=3600, user=user)
        mail_subject = 'Activate your Kaypay ccount.'
        context = {
            'user': user,
            'token': token}
        template_name = 'users/token_request.html'
        from_email = 'KayPay Onboarding Team <onboarding@kaypay.com>'
        to_email = user.email
        send_mail(subject=mail_subject, sender=from_email, receiver=[to_email],
                  context=context, template_name=template_name)
        user_token = self.get_tokens_for_user(user)
        response = {
            "refresh": user_token["refresh"],
            "access": user_token["access"],
            "user": serializer.data
        }

        return Response(response, status=status.HTTP_201_CREATED, headers=headers)

    @transaction.atomic
    def perform_create(self, serializer):
        instance = serializer.save()
        return instance

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class EmailVerificationView(generics.GenericAPIView):
    serializer_class = TokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = request.data.get("token")
        token_service = TokenService(token=token)
        token = token_service.verify_token()
        user = token.user
        user.active = True
        user.save()

        return Response(UserSerializer(user).data)

