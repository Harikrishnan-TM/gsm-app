from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from django.contrib.auth.models import User
from stocks.models import UserPortfolio







from django.contrib import messages

from website.models import MonthlyTournamentEntry
from website.models import UserProfile  # Adjust if path is different




from django.shortcuts import redirect






















from django.contrib import messages
from django.utils import timezone
from website.models import MonthlyTournamentEntry

import logging
from django.shortcuts import render


from .models import UserProfile



 # ✅ Import from the app where UserProfile is defined




# Set up logger
logger = logging.getLogger(__name__)

def home(request):
    profile = None
    is_trading_locked = False  # Default to locked if unauthenticated or profile not found

    try:
        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                is_trading_locked = profile.is_trading_locked  # ✅ Extract trading lock status
            except UserProfile.DoesNotExist:
                logger.warning(f"UserProfile not found for user {request.user.username}")
    except Exception as e:
        logger.exception("Unexpected error in home view")
        return render(request, 'website/home.html', {
            'profile': None,
            'error': 'An unexpected error occurred. Our team has been notified.',
            'is_trading_locked': True  # show locked state if error occurs
        })

    return render(request, 'website/home.html', {
        'profile': profile,
        'is_trading_locked': is_trading_locked  # ✅ Now available to template
    })






def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'website/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'website/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')





# website/views.py



@login_required
def profile_view(request):
    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'profile.html', {'profile': profile})



# website/views.py







@login_required
def join_tournament(request):
    now = timezone.now()

    # Round to nearest 10-minute block
    rounded_minute = (now.minute // 10) * 10
    start_time = now.replace(minute=rounded_minute, second=0, microsecond=0)
    tournament_key = f"{now.date()}-{rounded_minute:02d}"

    # Check if already joined
    already_joined = MonthlyTournamentEntry.objects.filter(
        user=request.user,
        tournament_key=tournament_key
    ).exists()

    if already_joined:
        messages.warning(request, "⚠️ You’ve already joined this tournament round.")
    else:
        # Reset balance and lock trading
        profile = UserProfile.objects.get(user=request.user)
        profile.balance = 10000
        profile.is_trading_locked = True
        profile.save()

        # Clear existing portfolio
        UserPortfolio.objects.filter(user=request.user).delete()

        # Create tournament entry
        MonthlyTournamentEntry.objects.create(
            user=request.user,
            tournament_key=tournament_key,
            start_time=start_time,
            starting_balance=profile.balance
        )

        messages.success(request, "✅ Successfully joined tournament! Game will begin shortly.")

    return redirect('home')










logger = logging.getLogger(__name__)

def leaderboard_api(request):
    try:
        now = timezone.now()

        # Round down to current 10-min block
        rounded_minute = (now.minute // 10) * 10
        tournament_key = f"{now.date()}-{rounded_minute:02d}"

        # If leaderboard not finalized yet, check previous block
        entries = MonthlyTournamentEntry.objects.filter(
            tournament_key=tournament_key,
            final_score__isnull=False
        )

        if not entries.exists():
            # Fallback to last completed tournament block
            fallback_minute = rounded_minute - 10
            if fallback_minute < 0:
                fallback_minute += 60
                now = now - timezone.timedelta(hours=1)
            tournament_key = f"{now.date()}-{fallback_minute:02d}"
            entries = MonthlyTournamentEntry.objects.filter(
                tournament_key=tournament_key,
                final_score__isnull=False
            )

        leaderboard = []

        for entry in entries:
            leaderboard.append({
                'username': entry.user.username,
                'final_score': float(entry.final_score),
            })

        leaderboard_sorted = sorted(leaderboard, key=lambda x: x['final_score'], reverse=True)
        return JsonResponse(leaderboard_sorted, safe=False)

    except Exception as e:
        logger.error("Error in leaderboard_api: %s", e, exc_info=True)
        return JsonResponse({'error': 'Internal server error'}, status=500)





@login_required
def leaderboard_view(request):
    return render(request, 'website/leaderboard.html')





@login_required
def get_trading_status(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
        return JsonResponse({'is_trading_locked': profile.is_trading_locked})
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'Profile not found'}, status=404)
