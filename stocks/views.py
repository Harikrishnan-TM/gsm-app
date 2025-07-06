from rest_framework import viewsets
from .models import VirtualStock, UserPortfolio, UserTransaction
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    VirtualStockSerializer,
    UserPortfolioSerializer,
    UserTransactionSerializer
)

class VirtualStockViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = VirtualStock.objects.all()
    serializer_class = VirtualStockSerializer

class UserPortfolioViewSet(viewsets.ModelViewSet):
    queryset = UserPortfolio.objects.all()  # Added for DRF router compatibility
    serializer_class = UserPortfolioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserPortfolio.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserTransactionViewSet(viewsets.ModelViewSet):
    queryset = UserTransaction.objects.all()  # Also added for safety
    serializer_class = UserTransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserTransaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
