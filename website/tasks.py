from celery import shared_task
from django.utils import timezone
from tournament.models import Tournament, TournamentEntry
from core.models import UserProfile  # Adjust if UserProfile is in another app

@shared_task
def unlock_trading_for_tournament():
    now = timezone.now()

    print(f"\n===== ⏰ Celery Task Triggered at {now} =====")
    print("🔍 Checking tournaments active at this moment...")

    # Fetch tournaments that are currently active
    active_tournaments = Tournament.objects.filter(start_time__lte=now, end_time__gte=now)

    if not active_tournaments.exists():
        print("⚠️ No active tournaments right now.")
        return

    unlocked = 0
    for tournament in active_tournaments:
        entries = TournamentEntry.objects.filter(tournament=tournament)

        for entry in entries:
            try:
                profile = UserProfile.objects.get(user=entry.user)
                if profile.is_trading_locked:
                    profile.is_trading_locked = False
                    profile.save()
                    unlocked += 1
                    print(f"✅ Trading unlocked for {entry.user.username} (Tournament ID: {tournament.id})")
            except UserProfile.DoesNotExist:
                print(f"❌ UserProfile not found for {entry.user.username}")

    print(f"🏁 Finished unlocking. Total users unlocked: {unlocked}\n")
