import time
from datetime import datetime

from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.exceptions import ValidationError

from users.services.token import TokenService
from users.models import Token

User = get_user_model()


class TokenServiceTest(TestCase):
    def setUp(self) -> None:
        self.user = User(email="dev@kaypay.com")
        self.user.set_password("password")
        self.user.save()
        self.token_service = TokenService()

    def test_generate_valid_token(self):
        token, expires_at = self.token_service.generate_token(user=self.user, seconds=60)
        self.assertIs(type(token), str)
        self.assertIs(type(expires_at), datetime)

    def test_verify_valid_token(self):
        token, expires_at = self.token_service.generate_token(user=self.user, seconds=60)
        self.token_service.token = token
        token_obj = self.token_service.verify_token()
        self.assertIs(type(token_obj), Token)
        self.assertEqual(token, token_obj.token)

    def test_token_expired(self):
        token, expires_at = self.token_service.generate_token(user=self.user, seconds=5)
        self.token_service.token = token
        time.sleep(10)
        with self.assertRaises(ValidationError):
            self.token_service.verify_token()
        with self.assertRaisesMessage(ValidationError, "Expired Token"):
            self.token_service.verify_token()

    def test_token_invalid_token(self):
        token, expires_at = self.token_service.generate_token(user=self.user, seconds=5)
        self.token_service.token = "invalid"
        with self.assertRaises(ValidationError):
            self.token_service.verify_token()
        with self.assertRaisesMessage(ValidationError, "Invalid Token"):
            self.token_service.verify_token()
