from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from django.contrib.auth.models import User
from stocks.models import UserPortfolio













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
    try:
        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
            except UserProfile.DoesNotExist:
                logger.warning(f"UserProfile not found for user {request.user.username}")
                profile = None  # Or create one if needed
    except Exception as e:
        logger.exception("Unexpected error in home view")
        # Optional: add a user-visible error message if desired
        return render(request, 'website/home.html', {
            'profile': None,
            'error': 'An unexpected error occurred. Our team has been notified.'
        })

    return render(request, 'website/home.html', {'profile': profile})






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
    month = now.month
    year = now.year

    already_joined = MonthlyTournamentEntry.objects.filter(
        user=request.user,
        month=month,
        year=year
    ).exists()

    if already_joined:
        messages.warning(request, "You have already joined this month's tournament.")
    else:
        MonthlyTournamentEntry.objects.create(
            user=request.user,
            month=month,
            year=year,
            starting_balance=request.user.userprofile.balance  # store balance at join time
        )
        messages.success(request, "✅ You have successfully joined the tournament!")

    return redirect('home')  # or wherever your home view is named






logger = logging.getLogger(__name__)

def leaderboard_api(request):
    try:
        leaderboard = []
        users = User.objects.all()

        for user in users:
            user_portfolio = UserPortfolio.objects.filter(user=user)

            total_value = 0
            total_cost = 0

            for holding in user_portfolio:
                # Convert Decimal to float for safe arithmetic
                current_price = float(holding.stock.current_price)
                total_value += current_price * holding.quantity
                total_cost += holding.average_price * holding.quantity

            leaderboard.append({
                'username': user.username,
                'portfolio_value': round(total_value, 2),
                'total_profit': round(total_value - total_cost, 2),
            })

        leaderboard_sorted = sorted(leaderboard, key=lambda x: x['portfolio_value'], reverse=True)
        return JsonResponse(leaderboard_sorted, safe=False)

    except Exception as e:
        logger.error("Error in leaderboard_api: %s", e, exc_info=True)
        return JsonResponse({'error': 'Internal server error'}, status=500)




@login_required
def leaderboard_view(request):
    return render(request, 'website/leaderboard.html')
