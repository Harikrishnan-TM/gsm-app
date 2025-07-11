from django.core.management.base import BaseCommand
from django.utils import timezone
from website.models import MonthlyTournamentEntry
from website.models import UserProfile

class Command(BaseCommand):
    help = 'Unlock trading for users when a tournament round starts'

    def handle(self, *args, **kwargs):
        now = timezone.now()

        # Round to current 10-minute block
        rounded_minute = (now.minute // 10) * 10
        current_block = now.replace(minute=rounded_minute, second=0, microsecond=0)
        tournament_key = f"{now.date()}-{rounded_minute:02d}"

        entries = MonthlyTournamentEntry.objects.filter(tournament_key=tournament_key)

        for entry in entries:
            profile = UserProfile.objects.get(user=entry.user)
            if profile.is_trading_locked:
                profile.is_trading_locked = False
                profile.save()
                self.stdout.write(f"✅ Trading unlocked for {entry.user.username}")
