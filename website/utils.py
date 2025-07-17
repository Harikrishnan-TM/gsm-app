
from website.models import UserProfile, Portfolio




def get_total_value(user, tournament):
    try:
        profile = UserProfile.objects.get(user=user)
        balance = profile.balance
    except UserProfile.DoesNotExist:
        balance = 0

    holdings = Portfolio.objects.filter(user=user, tournament=tournament)
    portfolio_value = sum(h.quantity * h.current_price for h in holdings)

    total_value = balance + portfolio_value
    return balance, portfolio_value, total_value
