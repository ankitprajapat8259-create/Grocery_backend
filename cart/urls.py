from django.urls import path
from .views import CartListView, CartAddView, CartUpdateView, CartRemoveView, CartClearView

urlpatterns = [
    path('', CartListView.as_view(), name='cart-list'),
    path('add/', CartAddView.as_view(), name='cart-add'),
    path('update/<int:id>/', CartUpdateView.as_view(), name='cart-update'),
    path('remove/<int:id>/', CartRemoveView.as_view(), name='cart-remove'),
    path('clear/', CartClearView.as_view(), name='cart-clear'),
]
