# core/models.py

from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.FloatField(default=10000.0)  # starting ₹10,000

    def __str__(self):
        return f"{self.user.username}'s Profile - ₹{self.balance}"
