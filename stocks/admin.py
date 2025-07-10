from django.contrib import admin
from .models import VirtualStock, UserPortfolio, UserTransaction
from .models import PriceHistory
from .models import Stock


admin.site.register(Stock)
admin.site.register(VirtualStock)
admin.site.register(UserPortfolio)
admin.site.register(UserTransaction)
admin.site.register(PriceHistory)  




