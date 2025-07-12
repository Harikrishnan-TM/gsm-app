from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from website.models import MonthlyTournamentEntry, UserProfile

class Command(BaseCommand):
    help = 'Unlock trading for users when a tournament round starts'

    def handle(self, *args, **kwargs):
        now = timezone.now()

        # Round to the nearest lower 10-minute block
        rounded_minute = (now.minute // 10) * 10
        current_block = now.replace(minute=rounded_minute, second=0, microsecond=0)

        # Also check previous block to handle cron delay
        previous_block = current_block - timedelta(minutes=10)

        # Generate both keys
        keys_to_check = [
            f"{current_block.date()}-{current_block.minute:02d}",
            f"{previous_block.date()}-{previous_block.minute:02d}"
        ]

        self.stdout.write(f"\n===== ⏰ Cron Triggered at {now} =====")
        self.stdout.write(f"🔑 Checking tournament keys: {keys_to_check}")

        entries = MonthlyTournamentEntry.objects.filter(tournament_key__in=keys_to_check)

        if not entries.exists():
            self.stdout.write("⚠️ No entries found to unlock.")
            return

        unlocked = 0
        for entry in entries:
            try:
                profile = UserProfile.objects.get(user=entry.user)
                if profile.is_trading_locked:
                    profile.is_trading_locked = False
                    profile.save()
                    unlocked += 1
                    self.stdout.write(f"✅ Trading unlocked for {entry.user.username}")
            except UserProfile.DoesNotExist:
                self.stdout.write(f"❌ UserProfile not found for user {entry.user.username}")

        self.stdout.write(f"🏁 Done. Total unlocked: {unlocked}\n")
