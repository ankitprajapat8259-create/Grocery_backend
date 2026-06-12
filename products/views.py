from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from .models import Product
from .serializers import ProductSerializer, ProductDetailSerializer, ProductSearchSerializer
from accounts.permissions import IsAdminRole


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(is_available=True)
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category']
    search_fields = ['name', 'description']
    
    @extend_schema(
        description="List all available products (Public)",
        responses={200: ProductSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ProductDetailSerializer
    lookup_field = 'id'
    
    @extend_schema(
        description="Get product details by ID (Public)",
        responses={200: ProductDetailSerializer},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ProductSearchView(generics.ListAPIView):
    queryset = Product.objects.filter(is_available=True)
    permission_classes = [AllowAny]
    serializer_class = ProductSearchSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name', 'description']
    
    @extend_schema(
        description="Search products by name or description (Public)",
        responses={200: ProductSearchSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class AdminProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated, IsAdminRole]
    serializer_class = ProductSerializer
    
    @extend_schema(
        description="Create a new product (Admin Only)",
        request=ProductSerializer,
        responses={201: ProductSerializer},
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AdminProductUpdateView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated, IsAdminRole]
    serializer_class = ProductSerializer
    lookup_field = 'id'
    
    @extend_schema(
        description="Update a product (Admin Only)",
        request=ProductSerializer,
        responses={200: ProductSerializer},
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    
    @extend_schema(
        description="Partially update a product (Admin Only)",
        request=ProductSerializer,
        responses={200: ProductSerializer},
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class AdminProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated, IsAdminRole]
    lookup_field = 'id'
    
    @extend_schema(
        description="Delete a product (Admin Only)",
        responses={204: None},
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
