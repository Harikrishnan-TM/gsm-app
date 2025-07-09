from django.core.management.base import BaseCommand
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal, ROUND_HALF_UP
import random

from stocks.models import VirtualStock, PriceHistory, UserTransaction


class Command(BaseCommand):
    help = 'Simulates stock market price changes based on user activity'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        window_start = now - timedelta(hours=1)

        for stock in VirtualStock.objects.all():
            # Aggregate user transactions in last 1 hour
            recent_transactions = UserTransaction.objects.filter(
                stock=stock,
                timestamp__gte=window_start
            ).values('transaction_type').annotate(total=Sum('quantity'))

            buy_qty = next((tx['total'] for tx in recent_transactions if tx['transaction_type'] == 'BUY'), 0) or 0
            sell_qty = next((tx['total'] for tx in recent_transactions if tx['transaction_type'] == 'SELL'), 0) or 0
            net_demand = buy_qty - sell_qty

            if net_demand == 0:
                # Random drift if no trading activity
                change_percent = Decimal(str(random.uniform(-0.005, 0.005)))  # ±0.5%
            else:
                # 0.1% per unit net demand, capped ±5%
                raw_pct = Decimal(net_demand) * Decimal('0.001')  # 0.1% per unit
                change_percent = max(Decimal('-0.05'), min(Decimal('0.05'), raw_pct))

            # Calculate new price
            new_price = stock.current_price * (Decimal('1.00') + change_percent)
            new_price = new_price.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

            # Enforce minimum price
            if new_price < Decimal('1.00'):
                new_price = Decimal('1.00')

            # Save new price
            stock.current_price = new_price
            stock.last_updated = now
            stock.save()

            # Save price history
            PriceHistory.objects.create(
                stock=stock.stock,
                price=new_price,
                timestamp=now
            )

            symbol = stock.stock.symbol
            self.stdout.write(
                self.style.SUCCESS(
                    f"{symbol}: ₹{stock.current_price} → ₹{new_price} "
                    f"(Buy: {buy_qty}, Sell: {sell_qty}, Δ: {net_demand})"
                )
            )
