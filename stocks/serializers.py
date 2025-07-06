from rest_framework import serializers
from .models import VirtualStock, UserPortfolio, UserTransaction

class VirtualStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = VirtualStock
        fields = '__all__'

class UserPortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPortfolio
        fields = '__all__'

class UserTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTransaction
        fields = '__all__'
