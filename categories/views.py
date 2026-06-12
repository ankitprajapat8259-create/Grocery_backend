from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .models import Category
from .serializers import CategorySerializer, CategoryDetailSerializer
from accounts.permissions import IsAdminRole


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    permission_classes = [AllowAny]
    serializer_class = CategorySerializer
    
    @extend_schema(
        description="List all categories (Public)",
        responses={200: CategorySerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    permission_classes = [AllowAny]
    serializer_class = CategoryDetailSerializer
    lookup_field = 'id'
    
    @extend_schema(
        description="Get category details by ID (Public)",
        responses={200: CategoryDetailSerializer},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class AdminCategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated, IsAdminRole]
    serializer_class = CategorySerializer
    
    @extend_schema(
        description="Create a new category (Admin Only)",
        request=CategorySerializer,
        responses={201: CategorySerializer},
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AdminCategoryUpdateView(generics.UpdateAPIView):
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated, IsAdminRole]
    serializer_class = CategorySerializer
    lookup_field = 'id'
    
    @extend_schema(
        description="Update a category (Admin Only)",
        request=CategorySerializer,
        responses={200: CategorySerializer},
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    
    @extend_schema(
        description="Partially update a category (Admin Only)",
        request=CategorySerializer,
        responses={200: CategorySerializer},
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class AdminCategoryDeleteView(generics.DestroyAPIView):
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated, IsAdminRole]
    lookup_field = 'id'
    
    @extend_schema(
        description="Delete a category (Admin Only)",
        responses={204: None},
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
