from rest_framework import serializers
from .models import Cart
from products.serializers import ProductSerializer


class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Cart
        fields = ['id', 'user', 'product', 'product_id', 'quantity', 'weight', 'subtotal', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'subtotal', 'created_at', 'updated_at']


class CartAddSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)
    weight = serializers.CharField(default='1kg')
    
    class Meta:
        model = Cart
        fields = ['product_id', 'quantity', 'weight']
    
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0.")
        return value


class CartUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['quantity']
    
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0.")
        return value
