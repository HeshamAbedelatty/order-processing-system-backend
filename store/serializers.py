from rest_framework import serializers
from .models import Product, Order


class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = '__all__'  # Include all fields

class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.ReadOnlyField(source='customer.username')
    
    class Meta:
        model = Order
        fields = ('id', 'customer','total_amount','paid', 'created_at')
        
# Payment Serializer for processing payments for orders 
class PaymentSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    card_number = serializers.CharField(max_length=16)  # Dummy data for testing
    expiry_date = serializers.CharField(max_length=5)  # Dummy data for testing
    cvv = serializers.CharField(max_length=3)  # Dummy data for testing
    order_id = serializers.IntegerField()