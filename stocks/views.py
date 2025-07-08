from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import VirtualStock, UserPortfolio, UserTransaction
from rest_framework.authentication import SessionAuthentication
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
    serializer_class = UserPortfolioSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]  # 👈 ADD THIS

    def get_queryset(self):
        return UserPortfolio.objects.filter(user=self.request.user).select_related('stock')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserTransactionViewSet(viewsets.ModelViewSet):
    serializer_class = UserTransactionSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]  # 👈 ADD THIS

    def get_queryset(self):
        return UserTransaction.objects.filter(user=self.request.user).select_related('stock')

    def perform_create(self, serializer):
        stock = serializer.validated_data['stock']
        quantity = serializer.validated_data['quantity']
        transaction_type = serializer.validated_data['transaction_type']
        price_at_execution = stock.stock.price

        serializer.save(
            user=self.request.user,
            stock=stock,
            quantity=quantity,
            transaction_type=transaction_type,
            price_at_execution=price_at_execution
        )
