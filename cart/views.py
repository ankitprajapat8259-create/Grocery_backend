from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .models import Cart
from .serializers import CartSerializer, CartAddSerializer, CartUpdateSerializer
from products.models import Product


class CartListView(generics.ListAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    
    @extend_schema(
        description="Get current user's cart items",
        responses={200: CartSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CartAddView(generics.CreateAPIView):
    serializer_class = CartAddSerializer
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        description="Add product to cart",
        request=CartAddSerializer,
        responses={201: CartSerializer},
    )
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            product_id = serializer.validated_data['product_id']
            quantity = serializer.validated_data.get('quantity', 1)
            weight = serializer.validated_data.get('weight', '1kg')
            
            try:
                product = Product.objects.get(id=product_id, is_available=True)
            except Product.DoesNotExist:
                return Response(
                    {'error': 'Product not found or not available'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Check if product is in stock
            if product.stock_quantity < quantity:
                return Response(
                    {'error': 'Insufficient stock'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Check if item already exists in cart with same weight
            cart_item, created = Cart.objects.get_or_create(
                user=request.user,
                product=product,
                weight=weight,
                defaults={'quantity': quantity}
            )
            
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            
            return Response(
                CartSerializer(cart_item).data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            print(f"Error adding to cart: {str(e)}")
            import traceback
            traceback.print_exc()
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CartUpdateView(generics.UpdateAPIView):
    serializer_class = CartUpdateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    
    @extend_schema(
        description="Update cart item quantity",
        request=CartUpdateSerializer,
        responses={200: CartSerializer},
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class CartRemoveView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    
    @extend_schema(
        description="Remove item from cart",
        responses={204: None},
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class CartClearView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    
    @extend_schema(
        description="Clear all items from cart",
        responses={204: None},
    )
    def delete(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
