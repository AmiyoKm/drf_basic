from django.contrib.auth.models import User
from django.db import models


class Transactions(models.Model):
    title = models.CharField(max_length=255)
    amount = models.FloatField()
    transaction_type = models.CharField(
        max_length=255, choices=(("CREDIT", "CREDIT"), ("DEBIT", "DEBIT"))
    )
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not isinstance(self.amount, (int, float)):
            raise ValueError("Amount must be a number")
        if self.transaction_type == "DEBIT":
            self.amount = -self.amount

        return super().save(*args, **kwargs)
