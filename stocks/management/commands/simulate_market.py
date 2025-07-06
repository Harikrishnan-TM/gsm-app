from django.core.management.base import BaseCommand
from stocks.models import VirtualStock
import random
from django.utils import timezone

class Command(BaseCommand):
    help = 'Simulates stock market price changes'

    def handle(self, *args, **kwargs):
        stocks = VirtualStock.objects.all()
        for stock in stocks:
            change_percent = random.uniform(-0.02, 0.02)
            new_price = stock.current_price * (1 + change_percent)
            stock.current_price = round(new_price, 2)
            stock.last_updated = timezone.now()
            stock.save()
            self.stdout.write(f"{stock.ticker} updated to ₹{stock.current_price}")
