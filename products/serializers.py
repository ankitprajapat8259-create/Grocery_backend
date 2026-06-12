from rest_framework import serializers
from .models import Product
from categories.serializers import CategorySerializer


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'category', 'category_id', 'name', 'description', 'image', 'price', 'stock_quantity', 'is_available', 'created_at']
        read_only_fields = ['id', 'created_at']


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'category', 'name', 'description', 'image', 'price', 'stock_quantity', 'is_available', 'created_at']
        read_only_fields = ['id', 'created_at']


class ProductSearchSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'category', 'name', 'description', 'image', 'price', 'stock_quantity', 'is_available']
