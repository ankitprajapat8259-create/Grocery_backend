from django.urls import path
from .views import (
    ProductListView,
    ProductDetailView,
    ProductSearchView,
    AdminProductCreateView,
    AdminProductUpdateView,
    AdminProductDeleteView,
)

urlpatterns = [
    # Public endpoints
    path('', ProductListView.as_view(), name='product-list'),
    path('<int:id>/', ProductDetailView.as_view(), name='product-detail'),
    path('search/', ProductSearchView.as_view(), name='product-search'),
    
    # Admin endpoints
    path('admin/create/', AdminProductCreateView.as_view(), name='admin-product-create'),
    path('admin/<int:id>/update/', AdminProductUpdateView.as_view(), name='admin-product-update'),
    path('admin/<int:id>/delete/', AdminProductDeleteView.as_view(), name='admin-product-delete'),
]
