from rest_framework import serializers
from src.item.models import Item


class ItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'brand_name']