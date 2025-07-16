# core/models.py or tournament/models.py (based on your app structure)

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.FloatField(default=10000.0)  # Starting ₹10,000
    is_trading_locked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Profile - ₹{self.balance}"


class Tournament(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"Tournament from {self.start_time.strftime('%Y-%m-%d %H:%M')} to {self.end_time.strftime('%H:%M')}"


class TournamentEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'tournament')
        ordering = ['-joined_at']

    def __str__(self):
        return f"{self.user.username} in {self.tournament}"



# Add to your core/models.py or tournament/models.py (wherever it fits best)

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)  # 🔥 Add this
    symbol = models.CharField(max_length=10)
    quantity = models.IntegerField()
    average_price = models.FloatField()
    current_price = models.FloatField()

    def __str__(self):
        return f"{self.user.username} - {self.symbol}: {self.quantity} @ ₹{self.average_price}"


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=10)
    quantity = models.IntegerField()
    price = models.FloatField()
    transaction_type = models.CharField(max_length=4, choices=[('BUY', 'Buy'), ('SELL', 'Sell')])
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} {self.quantity} {self.symbol} @ ₹{self.price}"
