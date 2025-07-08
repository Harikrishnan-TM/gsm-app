# stocks/serializers.py

from rest_framework import serializers
from .models import VirtualStock, UserPortfolio, UserTransaction

# ✅ Nested serializer for display
class VirtualStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = VirtualStock
        fields = ['id', 'symbol', 'name', 'price']

# ✅ Portfolio serializer using nested stock
class UserPortfolioSerializer(serializers.ModelSerializer):
    stock = VirtualStockSerializer(read_only=True)
    stock_id = serializers.PrimaryKeyRelatedField(
        queryset=VirtualStock.objects.all(), source='stock', write_only=True
    )

    class Meta:
        model = UserPortfolio
        fields = ['id', 'stock', 'stock_id', 'quantity']

# ✅ Transaction serializer with nested stock and write support
class UserTransactionSerializer(serializers.ModelSerializer):
    stock = VirtualStockSerializer(read_only=True)
    stock_id = serializers.PrimaryKeyRelatedField(
        queryset=VirtualStock.objects.all(), source='stock', write_only=True
    )

    class Meta:
        model = UserTransaction
        fields = ['id', 'stock', 'stock_id', 'action', 'quantity', 'price', 'timestamp']
