from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VirtualStockViewSet, UserPortfolioViewSet, UserTransactionViewSet



from .views import PriceHistoryView


router = DefaultRouter()
router.register(r'portfolio', UserPortfolioViewSet, basename='portfolio')
router.register(r'transactions', UserTransactionViewSet, basename='transaction')
router.register(r'stocks', VirtualStockViewSet, basename='stock')

urlpatterns = [
    path('', include(router.urls)),
    path('history/<str:symbol>/', PriceHistoryView.as_view(), name='price-history'),
   
]






