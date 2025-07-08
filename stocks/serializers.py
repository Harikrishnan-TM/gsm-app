from rest_framework import serializers
from .models import VirtualStock, UserPortfolio, UserTransaction


# ✅ Serializer for VirtualStock (used nested in others)
class VirtualStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = VirtualStock
        fields = ['id', 'symbol', 'name', 'price']


# ✅ Serializer for user portfolio with nested stock for read, and stock_id for write
class UserPortfolioSerializer(serializers.ModelSerializer):
    stock = VirtualStockSerializer(read_only=True)
    stock_id = serializers.PrimaryKeyRelatedField(
        queryset=VirtualStock.objects.all(),
        source='stock',
        write_only=True
    )

    class Meta:
        model = UserPortfolio
        fields = ['id', 'stock', 'stock_id', 'quantity']


# ✅ Serializer for user transaction with nested stock for read, and stock_id for write
class UserTransactionSerializer(serializers.ModelSerializer):
    stock = VirtualStockSerializer(read_only=True)
    stock_id = serializers.PrimaryKeyRelatedField(
        queryset=VirtualStock.objects.all(),
        source='stock',
        write_only=True
    )

    class Meta:
        model = UserTransaction
        fields = ['id', 'stock', 'stock_id', 'action', 'quantity', 'price', 'timestamp']
