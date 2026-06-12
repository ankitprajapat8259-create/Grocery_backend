from django.urls import path
from .views import (
    OrderListView,
    OrderDetailView,
    create_order,
    AdminOrderListView,
    AdminOrderStatusUpdateView,
)

urlpatterns = [
    # User endpoints
    path('create/', create_order, name='order-create'),
    path('', OrderListView.as_view(), name='order-list'),
    path('<int:id>/', OrderDetailView.as_view(), name='order-detail'),
    
    # Admin endpoints
    path('admin/all/', AdminOrderListView.as_view(), name='admin-order-list'),
    path('admin/<int:id>/status/', AdminOrderStatusUpdateView.as_view(), name='admin-order-status-update'),
]
