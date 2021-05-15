from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from wallets.models import Wallet

User = get_user_model()


class WalletModelTest(TestCase):
    def setUp(self) -> None:
        self.user = User(email="dev@kaypay.com")
        self.user.set_password("password")
        self.user.save()

    def test_wallet_create_success(self):
        wallet = Wallet.objects.create(user=self.user)
        self.assertIs(type(wallet), Wallet)
        self.assertEqual(wallet.balance, Decimal(0.00))

    def test_multiple_wallet(self):
        wallets = [
            {
                "balance": 900000
            },
            {
                "balance": 100000
            }
        ]
        wallet_objects = [Wallet(**obj, user=self.user) for obj in wallets]
        Wallet.objects.bulk_create(wallet_objects)
        wallet_fetched_qs = Wallet.objects.all()
        self.assertEqual(wallet_fetched_qs.count(), 2)
        self.assertEqual(wallets[0].get("balance"), 900000)
