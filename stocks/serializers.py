from rest_framework import serializers
from .models import VirtualStock, UserPortfolio, UserTransaction
from website.models import UserProfile  # ✅ Import the profile model



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

    average_price = serializers.SerializerMethodField()
    current_price = serializers.SerializerMethodField()
    profit_loss = serializers.SerializerMethodField()
    percentage_change = serializers.SerializerMethodField()

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
            'percentage_change',
        ]

    def get_average_price(self, obj):
        from .models import UserTransaction  # ✅ Use your actual model
        transactions = UserTransaction.objects.filter(
            user=obj.user,
            stock=obj.stock,
            transaction_type='BUY'
        )

        total_qty = sum(t.quantity for t in transactions)
        total_cost = sum(t.quantity * t.price_at_execution for t in transactions)

        if total_qty == 0:
            return 0.0

        return round(total_cost / total_qty, 2)

    def get_current_price(self, obj):
        return round(float(obj.stock.current_price), 2)

    def get_profit_loss(self, obj):
        average_price = self.get_average_price(obj)
        current_price = float(obj.stock.current_price)
        profit = (current_price - average_price) * obj.quantity
        return round(profit, 2)

    def get_percentage_change(self, obj):
        average_price = self.get_average_price(obj)
        if average_price == 0:
            return None
        current_price = float(obj.stock.current_price)
        return round(((current_price - average_price) / average_price) * 100, 2)




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
        read_only_fields = ['price_at_execution']

    def create(self, validated_data):
        stock = validated_data['stock']
        user = self.context['request'].user
        transaction_type = validated_data['transaction_type']
        quantity = validated_data['quantity']
        current_price = float(stock.current_price)

        validated_data['price_at_execution'] = current_price

        # ✅ Fetch the user's profile
        profile = UserProfile.objects.get(user=user)

        if transaction_type == 'BUY':
            total_cost = quantity * current_price
            if profile.balance < total_cost:
                raise serializers.ValidationError("❌ Insufficient balance.")
            profile.balance -= total_cost

        elif transaction_type == 'SELL':
            # ✅ Check if user has enough stock to sell
            from stocks.models import UserPortfolio  # Import here to avoid circular imports
            portfolio = UserPortfolio.objects.filter(user=user, stock=stock).first()

            if not portfolio or portfolio.quantity < quantity:
                raise serializers.ValidationError("❌ You do not have enough shares to sell.")

            profile.balance += quantity * current_price

        profile.save()

        validated_data['user'] = user
        return super().create(validated_data)