from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import VirtualStock, UserPortfolio, UserTransaction
from .serializers import (
    VirtualStockSerializer,
    UserPortfolioSerializer,
    UserTransactionSerializer
)


class VirtualStockViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Public endpoint to view available virtual stocks.
    """
    queryset = VirtualStock.objects.all()
    serializer_class = VirtualStockSerializer


class UserPortfolioViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for a user's stock holdings (portfolio).
    Only authenticated users can access their own portfolio.
    """
    serializer_class = UserPortfolioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserPortfolio.objects.filter(user=self.request.user).select_related('stock')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserTransactionViewSet(viewsets.ModelViewSet):
    """
    Create and view a user's stock buy/sell transactions.
    """
    serializer_class = UserTransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserTransaction.objects.filter(user=self.request.user).select_related('stock')

    def perform_create(self, serializer):
        stock = serializer.validated_data['stock']
        quantity = serializer.validated_data['quantity']
        transaction_type = serializer.validated_data['transaction_type']
        price_at_execution = stock.stock.price  # get real stock price at time of transaction

        serializer.save(
            user=self.request.user,
            stock=stock,
            quantity=quantity,
            transaction_type=transaction_type,
            price_at_execution=price_at_execution
        )
