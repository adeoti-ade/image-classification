from utils.helpers import token_generator

from django.utils import timezone

from users.models import Token
from rest_framework import serializers


class TokenService(object):
    """
    This class handles the generation of one time token for user verification
    """
    def __init__(self, token=None):
        self.token = token

    def generate_token(self, seconds, user=None):
        """
        This method handles generating a unique token for users
        :param seconds: the duration of the token validity
        :param user: the user the token is created for
        :return:
            token: the one time token for verificatio
            expires_at: time validity of the token
        """
        token, expires_at = token_generator(seconds=seconds)
        if user:
            user.token.create(expires=expires_at, token=token)
        return token, expires_at

    def verify_token(self):
        """
        This method handles verification of the validity of the token
        :raises validation error if not valid
        :return:
            token_obj: an object instance of the token
        """
        token_qs = Token.objects.filter(token=self.token)
        if not token_qs:
            raise serializers.ValidationError(detail={"token": "Invalid Token"})
        token_obj = token_qs.first()
        expires = token_obj.expires
        token_new, expires_at = token_generator(expires_at=expires)
        if timezone.now() > expires_at:
            raise serializers.ValidationError(detail={"token": "Expired Token"})

        if self.token != token_new:
            raise serializers.ValidationError(detail={"token": "Token does not match"})
        else:
            return token_obj
