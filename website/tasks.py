from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from website.models import MonthlyTournamentEntry, UserProfile

@shared_task
def unlock_trading_for_tournament():
    now = timezone.now()

    # Round to the nearest lower 10-minute block
    rounded_minute = (now.minute // 10) * 10
    current_block = now.replace(minute=rounded_minute, second=0, microsecond=0)

    # Also check previous block to handle delay
    previous_block = current_block - timedelta(minutes=10)

    # Generate both keys
    keys_to_check = [
        f"{current_block.date()}-{current_block.minute:02d}",
        f"{previous_block.date()}-{previous_block.minute:02d}"
    ]

    print(f"\n===== ⏰ Celery Task Triggered at {now} =====")
    print(f"🔑 Checking tournament keys: {keys_to_check}")

    entries = MonthlyTournamentEntry.objects.filter(tournament_key__in=keys_to_check)

    if not entries.exists():
        print("⚠️ No entries found to unlock.")
        return

    unlocked = 0
    for entry in entries:
        try:
            profile = UserProfile.objects.get(user=entry.user)
            if profile.is_trading_locked:
                profile.is_trading_locked = False
                profile.save()
                unlocked += 1
                print(f"✅ Trading unlocked for {entry.user.username}")
        except UserProfile.DoesNotExist:
            print(f"❌ UserProfile not found for user {entry.user.username}")

    print(f"🏁 Done. Total unlocked: {unlocked}\n")
