from django.db import models
from accounts.models import User
from products.models import Product
from decimal import Decimal


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    weight = models.CharField(max_length=20, default='1kg')  # Add weight field
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'cart'
        verbose_name = 'Cart'
        verbose_name_plural = 'Cart'
        unique_together = ['user', 'product', 'weight']  # Include weight in unique constraint
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.product.name} ({self.weight}) (Qty: {self.quantity})"
    
    def save(self, *args, **kwargs):
        # Calculate price based on weight
        try:
            weight_multiplier = {
                '250g': Decimal('0.25'),
                '500g': Decimal('0.5'),
                '1kg': Decimal('1'),
                '2kg': Decimal('2')
            }.get(self.weight, Decimal('1'))
            self.subtotal = self.product.price * weight_multiplier * self.quantity
        except Exception as e:
            print(f"Error calculating subtotal: {e}")
            self.subtotal = self.product.price * self.quantity
        super().save(*args, **kwargs)
