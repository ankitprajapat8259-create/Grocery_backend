from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'price', 'stock_quantity', 'is_available', 'created_at']
    list_filter = ['category', 'is_available', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['-created_at']
    
    fieldsets = (
        (None, {'fields': ('category', 'name', 'description', 'image', 'price', 'stock_quantity', 'is_available')}),
        ('Timestamps', {'fields': ('created_at',)}),
    )
    readonly_fields = ['created_at']
