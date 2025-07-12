

# Create your models here.

# core/models.py

from django.contrib.auth.models import User
from django.db import models


from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.FloatField(default=10000.0)  # starting ₹10,000
    is_trading_locked = models.BooleanField(default=False)  # ✅ Add this line

    def __str__(self):
        return f"{self.user.username}'s Profile - ₹{self.balance}"



# tournament/models.py



class MonthlyTournamentEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.IntegerField()  # 1 = January, ..., 12 = December
    year = models.IntegerField()
    joined_on = models.DateTimeField(auto_now_add=True)
    starting_balance = models.DecimalField(max_digits=12, decimal_places=2, default=10000.00)
    tournament_key = models.CharField(max_length=50)  # e.g., '2025-07-11-10'
    start_time = models.DateTimeField(null=True, blank=True)  # ✅ Add this
    active = models.BooleanField(default=True)
    final_score = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = ('user', 'tournament_key')  # ✅ Updated for per-round tracking
        ordering = ['-year', '-month']

    def __str__(self):
        return f"{self.user.username} - {self.tournament_key}"





