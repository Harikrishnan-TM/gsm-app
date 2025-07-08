from rest_framework import serializers
from .models import VirtualStock, UserPortfolio, UserTransaction


# ✅ Serializer for VirtualStock with derived fields from related Stock
class VirtualStockSerializer(serializers.ModelSerializer):
    symbol = serializers.CharField(source='stock.symbol', read_only=True)
    name = serializers.CharField(source='stock.name', read_only=True)
    price = serializers.DecimalField(source='stock.price', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = VirtualStock
        fields = ['id', 'symbol', 'name', 'price']


# ✅ Serializer for UserPortfolio with nested VirtualStock
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


# ✅ Serializer for UserTransaction with proper field names
class UserTransactionSerializer(serializers.ModelSerializer):
    stock = VirtualStockSerializer(read_only=True)
    stock_id = serializers.PrimaryKeyRelatedField(
        queryset=VirtualStock.objects.all(),
        source='stock',
        write_only=True
    )

    class Meta:
        model = UserTransaction
        fields = ['id', 'stock', 'stock_id', 'transaction_type', 'quantity', 'price_at_execution', 'timestamp']
        read_only_fields = ['price_at_execution']  # ✅ add this line