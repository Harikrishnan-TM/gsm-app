from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from .models import VirtualStock, UserPortfolio, UserTransaction
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import PriceHistory
from django.utils.timezone import now, timedelta

# views.py


from stocks.models import VirtualStock, PriceHistory
from django.shortcuts import get_object_or_404

from .serializers import (
    VirtualStockSerializer,
    UserPortfolioSerializer,
    UserTransactionSerializer
)
from django.db.models import F
from django.core.exceptions import ValidationError


class VirtualStockViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Public endpoint to view available virtual stocks.
    """
    queryset = VirtualStock.objects.all()
    serializer_class = VirtualStockSerializer


class UserPortfolioViewSet(viewsets.ModelViewSet):
    serializer_class = UserPortfolioSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def get_queryset(self):
        return UserPortfolio.objects.filter(user=self.request.user).select_related('stock')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserTransactionViewSet(viewsets.ModelViewSet):
    serializer_class = UserTransactionSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def get_queryset(self):
        return UserTransaction.objects.filter(user=self.request.user).select_related('stock')

    def perform_create(self, serializer):
        user = self.request.user
        stock = serializer.validated_data['stock']
        quantity = serializer.validated_data['quantity']
        transaction_type = serializer.validated_data['transaction_type']
        price_at_execution = stock.stock.price  # get real stock price at time of transaction

        # Save the transaction
        transaction = serializer.save(
            user=user,
            stock=stock,
            quantity=quantity,
            transaction_type=transaction_type,
            price_at_execution=price_at_execution
        )

        # Update the user's portfolio
        portfolio_entry, created = UserPortfolio.objects.get_or_create(
            user=user,
            stock=stock,
            defaults={'quantity': 0}
        )

        if transaction_type == 'BUY':
            portfolio_entry.quantity = F('quantity') + quantity
        elif transaction_type == 'SELL':
            if portfolio_entry.quantity < quantity:
                raise ValidationError("Not enough stock to sell.")
            portfolio_entry.quantity = F('quantity') - quantity

        portfolio_entry.save()
        portfolio_entry.refresh_from_db()





#class PriceHistoryView(APIView):
    #def get(self, request, symbol):
        # Get last 24 hours of price history
        #from stocks.models import Stock
        #try:
            #stock = Stock.objects.get(symbol=symbol)
        #except Stock.DoesNotExist:
            #return Response({"error": "Stock not found"}, status=404)

        #data = PriceHistory.objects.filter(stock=stock, timestamp__gte=now()-timedelta(hours=24)) \
            #.order_by('timestamp') \
            #.values('timestamp', 'price')

        #return Response(data)






class PriceHistoryView(APIView):
    def get(self, request, symbol):
        stock = get_object_or_404(VirtualStock, symbol=symbol)
        history = PriceHistory.objects.filter(stock=stock).order_by('-timestamp')[:30]
        data = [{
            'timestamp': h.timestamp.isoformat(),
            'price': float(h.price)
        } for h in reversed(history)]
        return Response(data)
