

from django.db import models
from django.contrib.auth.models import User

class VirtualStock(models.Model):
    name = models.CharField(max_length=100)
    ticker = models.CharField(max_length=10, unique=True)
    current_price = models.FloatField(default=100.0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.ticker} - ₹{self.current_price:.2f}"


class UserPortfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(VirtualStock, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    average_price = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.user.username} - {self.stock.ticker} ({self.quantity})"


class UserTransaction(models.Model):
    TRANSACTION_TYPES = (
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(VirtualStock, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPES)
    quantity = models.PositiveIntegerField()
    price_at_execution = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} {self.transaction_type} {self.stock.ticker} x{self.quantity} @ ₹{self.price_at_execution}"
