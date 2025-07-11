from django.core.management.base import BaseCommand
from django.utils import timezone
from website.models import MonthlyTournamentEntry
from stocks.models import UserPortfolio
from website.models import UserProfile

class Command(BaseCommand):
    help = 'Finalize tournament by calculating scores and locking trading'

    def handle(self, *args, **kwargs):
        now = timezone.now()

        # Get previous block (ended 10 mins ago)
        rounded_minute = ((now.minute // 10) * 10) - 10
        if rounded_minute < 0:
            rounded_minute += 60
            now = now - timezone.timedelta(hours=1)
        tournament_key = f"{now.date()}-{rounded_minute:02d}"

        entries = MonthlyTournamentEntry.objects.filter(tournament_key=tournament_key, final_score__isnull=True)

        for entry in entries:
            user = entry.user
            portfolio = UserPortfolio.objects.filter(user=user)

            total_value = 0
            for holding in portfolio:
                total_value += holding.stock.current_price * holding.quantity

            entry.final_score = round(total_value, 2)
            entry.save()

            # Optionally lock trading again
            profile = UserProfile.objects.get(user=user)
            profile.is_trading_locked = True
            profile.save()

            self.stdout.write(f"🏁 Finalized {user.username} — ₹{entry.final_score}")
