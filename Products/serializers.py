from rest_framework import serializers
from .models import Product
from .models import Categories
class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "description",
            "stock",        # added
            "category",     # added
            "owner",
            "created_at"
        ]
class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = [
            "name",
            "description"
        ]