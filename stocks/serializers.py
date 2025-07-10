from rest_framework import serializers
from .models import VirtualStock, UserPortfolio, UserTransaction


# ✅ Serializer for VirtualStock with derived fields from related Stock
class VirtualStockSerializer(serializers.ModelSerializer):
    symbol = serializers.CharField(source='stock.symbol', read_only=True)
    name = serializers.CharField(source='stock.name', read_only=True)
    price = serializers.DecimalField(source='current_price', max_digits=10, decimal_places=2, read_only=True)

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

    average_price = serializers.FloatField(read_only=True)
    current_price = serializers.SerializerMethodField()
    profit_loss = serializers.SerializerMethodField()
    percentage_change = serializers.SerializerMethodField()  # ← Add this field

    class Meta:
        model = UserPortfolio
        fields = [
            'id',
            'stock',
            'stock_id',
            'quantity',
            'average_price',
            'current_price',
            'profit_loss',
            'percentage_change',  # ← Include in fields
        ]

    def get_current_price(self, obj):
        return round(obj.stock.stock.price, 2)

    def get_profit_loss(self, obj):
        current_price = obj.stock.stock.price
        profit = (current_price - obj.average_price) * obj.quantity
        return round(profit, 2)

    def get_percentage_change(self, obj):
        if obj.average_price == 0:
            return 0.0
        current_price = obj.stock.stock.price
        return round(((current_price - obj.average_price) / obj.average_price) * 100, 2)



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