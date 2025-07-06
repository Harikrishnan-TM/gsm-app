from django.contrib import admin
from .models import VirtualStock, UserPortfolio, UserTransaction

admin.site.register(VirtualStock)
admin.site.register(UserPortfolio)
admin.site.register(UserTransaction)
