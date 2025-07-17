from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
import logging
from website.utils import get_total_value



from website.models import Tournament



from django.db.models import Sum


from django.db.models import F, Sum, FloatField, ExpressionWrapper
from .models import Portfolio, UserProfile  # adjust imports as needed

from .models import (
    UserProfile as Profile,
    Tournament,
    TournamentEntry,
    Portfolio,
    Transaction,
)






def get_portfolio_value(user, tournament):
    try:
        profile = UserProfile.objects.get(user=user)
        cash = profile.balance

        holdings = Portfolio.objects.filter(user=user, tournament=tournament).annotate(
            holding_value=ExpressionWrapper(F('quantity') * F('current_price'), output_field=FloatField())
        ).aggregate(total=Sum('holding_value'))

        holdings_value = holdings['total'] or 0
        return round(cash + holdings_value, 2)
    except UserProfile.DoesNotExist:
        return 0







logger = logging.getLogger(__name__)

# ---------------------- AUTH ----------------------

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
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'website/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')


# ---------------------- HOME ----------------------

def home(request):
    profile = None
    is_trading_locked = True
    has_joined_tournament = False

    try:
        if request.user.is_authenticated:
            profile = Profile.objects.get(user=request.user)

            now = timezone.now()
            current_entry = TournamentEntry.objects.filter(
                user=request.user
            ).order_by('-tournament__start_time').first()

            if current_entry:
                tournament = current_entry.tournament
                is_trading_locked = not (tournament.start_time <= now <= tournament.end_time)
                has_joined_tournament = True

    except Profile.DoesNotExist:
        logger.warning(f"No profile found for user {request.user.username}")

    except Exception as e:
        logger.exception("Error loading home view")

    return render(request, 'website/home.html', {
        'profile': profile,
        'is_trading_locked': is_trading_locked,
        'has_joined_tournament': has_joined_tournament,
    })


# ---------------------- PROFILE ----------------------

@login_required
def profile_view(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'profile.html', {'profile': profile})


# ---------------------- TOURNAMENT ----------------------

@login_required
def join_tournament(request):
    user = request.user
    now = timezone.now()

    minutes_to_next_10 = (10 - (now.minute % 10)) % 10
    next_slot = (now + timedelta(minutes=minutes_to_next_10)).replace(second=0, microsecond=0)
    end_time = next_slot + timedelta(minutes=10)

    tournament, _ = Tournament.objects.get_or_create(
        start_time=next_slot, end_time=end_time
    )

    TournamentEntry.objects.filter(user=user).delete()  # Remove old entry
    TournamentEntry.objects.create(user=user, tournament=tournament)

    profile = Profile.objects.get(user=user)
    profile.balance = 10000
    profile.save()

    Portfolio.objects.filter(user=user).delete()
    Transaction.objects.filter(user=user).delete()

    messages.success(request, "✅ Joined tournament! Game starts soon.")
    return redirect('home')


@login_required
def is_trading_locked(request):
    user = request.user
    now = timezone.now()

    entry = TournamentEntry.objects.filter(user=user).order_by('-tournament__start_time').first()
    if not entry:
        return JsonResponse({'is_trading_locked': True})

    tournament = entry.tournament
    is_locked = not (tournament.start_time <= now <= tournament.end_time)

    return JsonResponse({
        'is_trading_locked': is_locked,
        'starts_in': max(0, int((tournament.start_time - now).total_seconds())),
        'ends_in': max(0, int((tournament.end_time - now).total_seconds())),
    })


@login_required
def leaderboard_view(request):
    latest_tournament = Tournament.objects.order_by('-start_time').first()
    entries = TournamentEntry.objects.filter(tournament=latest_tournament)

    leaderboard = []
    for entry in entries:
        portfolio_value = get_portfolio_value(entry.user)
        leaderboard.append({
            'user': entry.user.username,
            'total': portfolio_value,
        })

    leaderboard.sort(key=lambda x: x['total'], reverse=True)
    return render(request, 'website/leaderboard.html', {'leaderboard': leaderboard})






logger = logging.getLogger(__name__)



@login_required
def leaderboard_page(request):
    latest_tournament = Tournament.objects.order_by('-start_time').first()

    # Default values in case something goes wrong
    current_value = 0

    if latest_tournament:
        try:
            balance, portfolio_value, total_value = get_total_value(request.user, latest_tournament)
            current_value = round(total_value, 2)
        except Exception as e:
            logger.warning(f"Could not compute current value for user {request.user.username}: {e}")

    return render(request, 'leaderboard.html', {
        'tournament': latest_tournament,
        'current_value': current_value
    })







