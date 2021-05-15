from users.api.validators import is_valid_mobile, valid_mobile_prefix
from rest_framework.exceptions import ValidationError
from django.test import TestCase


class MobileNumberTest(TestCase):
    def setUp(self):
        pass

    def test_mobile_length(self):
        with self.assertRaises(ValidationError):
            is_valid_mobile("10101023")
        with self.assertRaises(ValidationError):
            is_valid_mobile("123456789012333")

    def test_valid_prefix(self):
        with self.assertRaises(ValidationError):
            is_valid_mobile("01234567891")
            # msg = "mobile must be one of {}".format(",".join(valid_mobile_prefix))
        with self.assertRaises(ValidationError):
            is_valid_mobile("1234567890123")
