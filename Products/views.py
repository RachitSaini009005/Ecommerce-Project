from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.core.cache import cache

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Product, Categories
from .serializers import ProductSerializer, CategoriesSerializer
from .permissions import IsAdminOrOwnerOrReadOnly

User = get_user_model()


class ProductViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for Products with caching, pagination, and filtering.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrOwnerOrReadOnly]

    def list(self, request, *args, **kwargs):
        # Generate a unique cache key per URL including query params
        cache_key = f"products_{request.get_full_path()}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        # Get queryset with category to optimize queries
        queryset = self.filter_queryset(self.get_queryset().select_related('category'))

        # Pagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            cache.set(cache_key, serializer.data, timeout=3600)  # Cache for 1 hour
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        cache.set(cache_key, serializer.data, timeout=3600)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save()
        cache.clear()  # Clear all cache to reflect new product

    def perform_update(self, serializer):
        serializer.save()
        cache.clear()  # Clear cache on update

    def perform_destroy(self, instance):
        instance.delete()
        cache.clear()  # Clear cache on delete


class CategoryViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for Categories.
    """
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [IsAdminOrOwnerOrReadOnly]

    def perform_create(self, serializer):
        # Tag the category with the user who created it
        serializer.save(owner=self.request.user)
