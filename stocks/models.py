from django.db import models
from django.contrib.auth.models import User


class Stock(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.symbol} - {self.name}"


class VirtualStock(models.Model):
    stock = models.OneToOneField(Stock, on_delete=models.CASCADE)  # 1-to-1 with real stock
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.stock.symbol} - ₹{self.current_price}"


class UserPortfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(VirtualStock, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    average_price = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.user.username} - {self.stock.stock.symbol} ({self.quantity})"


class UserTransaction(models.Model):
    TRANSACTION_TYPES = (
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(VirtualStock, on_delete=models.CASCADE, null=True, blank=True)
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPES)
    quantity = models.PositiveIntegerField()
    price_at_execution = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        stock_symbol = self.stock.stock.symbol if self.stock else "N/A"
        return f"{self.user.username} {self.transaction_type} {stock_symbol} x{self.quantity} @ ₹{self.price_at_execution}"


class PriceHistory(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.stock.symbol} - ₹{self.price} @ {self.timestamp}"
