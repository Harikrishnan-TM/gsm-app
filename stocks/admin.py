from django.contrib import admin
from .models import VirtualStock, UserPortfolio, UserTransaction
from .models import PriceHistory

admin.site.register(VirtualStock)
admin.site.register(UserPortfolio)
admin.site.register(UserTransaction)
admin.site.register(PriceHistory)  
