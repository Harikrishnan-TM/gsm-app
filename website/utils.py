# tournament/utils.py (or wherever your app is)
from .models import Profile, Portfolio  # adjust the import based on your structure

def get_total_value(user, tournament):
    try:
        profile = Profile.objects.get(user=user)
        balance = profile.balance
    except Profile.DoesNotExist:
        balance = 0

    holdings = Portfolio.objects.filter(user=user, tournament=tournament).select_related('stock')
    portfolio_value = sum(h.quantity * h.stock.price for h in holdings)

    total_value = balance + portfolio_value
    return total_value
