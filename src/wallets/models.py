from django.db import models
from django.contrib.auth import get_user_model

from utils.models import BaseModel

User = get_user_model()


class Wallet(BaseModel):
    """
    This is the class that defines the wallet table schema
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wallets")
    balance = models.DecimalField(max_digits=100, decimal_places=2, null=False, default=0.00)

    class Meta:
        ordering = ("-created", )

    def __str__(self):
        return str(self.user.email)


class Transaction(BaseModel):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="transactions")
    narration = models.CharField(max_length=255, null=True)
    credit = models.DecimalField(max_digits=100, decimal_places=2, null=False, default=0.00)
    debit = models.DecimalField(max_digits=100, decimal_places=2, null=False, default=0.00)
    balance = models.DecimalField(max_digits=100, decimal_places=2, null=False, default=0.00)
    category = models.CharField(max_length=100, null=True)

    class Meta:
        ordering = ("-created", )

    def __str__(self):
        return self.wallet




