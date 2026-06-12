from django.urls import path
from .views import (
    CategoryListView,
    CategoryDetailView,
    AdminCategoryCreateView,
    AdminCategoryUpdateView,
    AdminCategoryDeleteView,
)

urlpatterns = [
    # Public endpoints
    path('', CategoryListView.as_view(), name='category-list'),
    path('<int:id>/', CategoryDetailView.as_view(), name='category-detail'),
    
    # Admin endpoints
    path('admin/create/', AdminCategoryCreateView.as_view(), name='admin-category-create'),
    path('admin/<int:id>/update/', AdminCategoryUpdateView.as_view(), name='admin-category-update'),
    path('admin/<int:id>/delete/', AdminCategoryDeleteView.as_view(), name='admin-category-delete'),
]
