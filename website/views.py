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

from .models import UserProfile



 # ✅ Import from the app where UserProfile is defined

def home(request):
    profile = None
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            profile = None  # Optional fallback, or you could create one here
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






def leaderboard_api(request):
    leaderboard = []

    users = User.objects.all()

    for user in users:
        user_portfolio = Portfolio.objects.filter(user=user)

        total_value = 0
        total_cost = 0

        for holding in user_portfolio:
            total_value += holding.current_price * holding.quantity
            total_cost += holding.average_price * holding.quantity

        leaderboard.append({
            'username': user.username,
            'portfolio_value': round(total_value, 2),
            'total_profit': round(total_value - total_cost, 2),
        })

    # Sort by portfolio value (highest first)
    leaderboard_sorted = sorted(leaderboard, key=lambda x: x['portfolio_value'], reverse=True)

    return JsonResponse(leaderboard_sorted, safe=False)





@login_required
def leaderboard_view(request):
    return render(request, 'website/leaderboard.html')
