from django.urls import path
from .views import dashboard_stats, user_list, toggle_user_status

urlpatterns = [
    path('dashboard/', dashboard_stats, name='dashboard-stats'),
    path('users/', user_list, name='admin-user-list'),
    path('users/<int:user_id>/toggle-status/', toggle_user_status, name='admin-toggle-user-status'),
]
