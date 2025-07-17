from decimal import Decimal
from stocks.models import UserPortfolio  # adjust this import as needed
from website.models import UserProfile   # ✅ import this too

def get_total_value(user, tournament=None):
    try:
        profile = UserProfile.objects.get(user=user)
        balance = Decimal(profile.balance)
    except UserProfile.DoesNotExist:
        balance = Decimal(0)

    # Get all holdings for the user
    holdings = UserPortfolio.objects.filter(user=user).select_related('stock__stock')

    # Compute portfolio value from live prices
    portfolio_value = sum(
        h.quantity * h.stock.current_price
        for h in holdings
        if h.stock and h.stock.current_price is not None
    )

    total_value = balance + portfolio_value
    return float(balance), float(portfolio_value), float(total_value)
