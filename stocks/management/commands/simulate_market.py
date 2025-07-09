from django.core.management.base import BaseCommand
from stocks.models import VirtualStock, PriceHistory
import random
from django.utils import timezone
from decimal import Decimal

class Command(BaseCommand):
    help = 'Simulates stock market price changes'

    def handle(self, *args, **kwargs):
        stocks = VirtualStock.objects.all()
        for stock in stocks:
            change_percent = random.uniform(-0.02, 0.02)  # -2% to +2%
            new_price = stock.current_price * Decimal(1 + change_percent)
            new_price = round(new_price, 2)

            # Update stock
            stock.current_price = new_price
            stock.last_updated = timezone.now()
            stock.save()

            # Save price history
            PriceHistory.objects.create(
                stock=stock.stock,
                price=new_price
            )

            symbol = getattr(stock.stock, 'symbol', 'N/A')
            self.stdout.write(f"{symbol} updated to ₹{new_price}")
