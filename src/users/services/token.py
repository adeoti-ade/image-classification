from utils.helpers import token_generator

from django.utils import timezone

from users.models import Token
from rest_framework import serializers


class TokenService(object):
    def __init__(self, token=None):
        self.token = token

    def generate_token(self, seconds, user=None):
        token, expires_at = token_generator(seconds=seconds)
        if user:
            user.token.create(expires=expires_at, otp=token)
        return token, expires_at

    def verify_token(self):
        token_qs = Token.objects.filter(otp=self.token)
        if not token_qs:
            raise serializers.ValidationError(detail={"token": "Invalid Token"})
        token_obj = token_qs.first()
        expires_at = token_obj.expires_at
        token_new, expires_at = token_generator(expires_at=expires_at)
        if timezone.now() > expires_at:
            raise serializers.ValidationError(detail={"otp": "Expired Token"})

        if self.token != token_new:
            raise serializers.ValidationError(detail={"otp": "Expired Token"})
        else:
            return token_obj
