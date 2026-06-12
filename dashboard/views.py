from django.db import models
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from accounts.models import User
from categories.models import Category
from products.models import Product
from orders.models import Order
from accounts.permissions import IsAdminRole


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminRole])
@extend_schema(
    description="Get admin dashboard statistics (Admin Only)",
    responses={200: {"type": "object"}},
)
def dashboard_stats(request):
    total_users = User.objects.count()
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_categories = Category.objects.count()
    
    # Calculate total revenue from delivered orders
    total_revenue = Order.objects.filter(
        order_status='Delivered'
    ).aggregate(total=models.Sum('total_amount'))['total'] or 0
    
    return Response({
        'total_users': total_users,
        'total_products': total_products,
        'total_orders': total_orders,
        'total_categories': total_categories,
        'total_revenue': total_revenue
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminRole])
@extend_schema(
    description="Get all users list (Admin Only)",
    responses={200: {"type": "array"}},
)
def user_list(request):
    from accounts.serializers import UserSerializer
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsAdminRole])
@extend_schema(
    description="Block/Unblock a user (Admin Only)",
    request={"type": "object", "properties": {"is_active": {"type": "boolean"}}},
    responses={200: {"type": "object"}},
)
def toggle_user_status(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.is_active = not user.is_active
        user.save()
        return Response({
            'message': f'User {"blocked" if not user.is_active else "unblocked"} successfully',
            'is_active': user.is_active
        })
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)
