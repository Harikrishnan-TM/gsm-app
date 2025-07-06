from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VirtualStockViewSet, UserPortfolioViewSet, UserTransactionViewSet

router = DefaultRouter()
router.register(r'stocks', VirtualStockViewSet)
router.register(r'portfolio', UserPortfolioViewSet)
router.register(r'transactions', UserTransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
