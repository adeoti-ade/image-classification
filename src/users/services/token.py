from users.models import Token
from django.utils import timezone
from rest_framework import serializers
from utils.helpers import token_generator


def generate_token(seconds, user=None):
    token, expires_at = token_generator(seconds=seconds)
    if user:
        user.token.create(expires=expires_at, otp=otp)
    return token, expires_at


def verify_token(token):
    token_qs = Token.objects.filter(otp=token)
    if not token_qs:
        raise serializers.ValidationError(detail={"otp": "Invalid Token"})
    token_obj = token_qs.first()
    expires_at = token_obj.expires_at
    token_new, expires_at = token_generator(expires_at=expires_at)
    if timezone.now() > expires_at:
        raise serializers.ValidationError(detail={"otp": "Expired Token"})

    if token == token_new:
        return token_obj, True
    else:
        return None, False
