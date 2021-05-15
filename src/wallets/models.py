from django.db import models
from django.contrib.auth import get_user_model

from utils.models import BaseModel

User = get_user_model()


class Wallet(BaseModel):
    """
    This is the class that defines the wallet table schema
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wallet")
    balance = models.DecimalField(max_digits=100, decimal_places=2, null=False, default=0.00)

    class Meta:
        ordering = ("-created", )

    def __str__(self):
        return self.user.email


