from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from drf_spectacular.utils import extend_schema
from django.db import transaction
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderCreateSerializer, OrderStatusUpdateSerializer
from cart.models import Cart
from accounts.permissions import IsAdminRole


class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    @extend_schema(
        description="Get current user's orders",
        responses={200: OrderSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    @extend_schema(
        description="Get order details by ID",
        responses={200: OrderSerializer},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@extend_schema(
    description="Create a new order from cart items",
    request=OrderCreateSerializer,
    responses={201: OrderSerializer},
)
def create_order(request):
    cart_items = Cart.objects.filter(user=request.user)
    
    if not cart_items.exists():
        return Response(
            {'error': 'Cart is empty'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check stock availability
    for cart_item in cart_items:
        if cart_item.product.stock_quantity < cart_item.quantity:
            return Response(
                {'error': f'Insufficient stock for {cart_item.product.name}'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    # Create order with transaction
    with transaction.atomic():
        total_amount = sum(item.subtotal for item in cart_items)
        order = Order.objects.create(
            user=request.user,
            total_amount=total_amount,
            order_status='Pending'
        )
        
        # Create order items and update stock
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            
            # Update product stock
            cart_item.product.stock_quantity -= cart_item.quantity
            cart_item.product.save()
        
        # Clear cart
        cart_items.delete()
    
    return Response(
        OrderSerializer(order).data,
        status=status.HTTP_201_CREATED
    )


class AdminOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]
    queryset = Order.objects.all()
    
    @extend_schema(
        description="Get all orders (Admin Only)",
        responses={200: OrderSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class AdminOrderStatusUpdateView(generics.UpdateAPIView):
    serializer_class = OrderStatusUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]
    queryset = Order.objects.all()
    lookup_field = 'id'
    
    @extend_schema(
        description="Update order status (Admin Only)",
        request=OrderStatusUpdateSerializer,
        responses={200: OrderSerializer},
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
