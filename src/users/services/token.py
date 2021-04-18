import string
import random
import six

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from users.models import Token
from datetime import timedelta
from django.utils import timezone
from rest_framework import serializers


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                six.text_type(user.pk) + six.text_type(timestamp) +
                six.text_type(user.is_active)
        )


class TokenGenerator:

    def otp_generator(self, size=6, chars=string.ascii_uppercase + string.digits, seconds=None, expires_at=None):
        """
        Generates a random string by using a time object as the seed \n

        parameters:
            size (int): The number of string to be generated
            chars (Fixed): A random generated ascii and digits generated from the string module and concatenated together
            seconds (int): A specified number of seconds the token is expected to last for
            expires_at (datetime): A specified timestamp at which the token is expected to expire
        returns:
            token: the generated token
            expires_at: The specified or timestamp at which the token is expected to expire
        """
        if not expires_at:
            expires_at = timezone.now() + timedelta(seconds=seconds)
        random.seed(expires_at)
        return ''.join(random.choice(chars) for _ in range(size)), expires_at

    def generate_otp(self, seconds, user=None):
        otp, expires_at = self.otp_generator(seconds=seconds)
        if user:
            user.token.create(expires=expires_at, otp=otp)
        return otp, expires_at

    def verify_otp(self, otp):
        token_qs = Token.objects.filter(otp=otp)
        if not token_qs:
            raise serializers.ValidationError(detail={"otp": "Invalid Token"})
        token_obj = token_qs.first()
        expires_at = token_obj.expires_at
        otp_new, expires_at = self.otp_generator(expires_at=expires_at)
        if timezone.now() > expires_at:
            raise serializers.ValidationError(detail={"otp": "Expired Token"})

        if otp == otp_new:
            return True
        else:
            return False
