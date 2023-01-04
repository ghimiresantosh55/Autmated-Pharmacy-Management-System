from rest_framework.utils import field_mapping
from .models import Location
from src.purchase.models import PurchaseDetail
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers


class LocationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        exclude = ['lft', 'rght', 'tree_id']



class LocationUpdateSerializer(serializers.Serializer):
    purchase_detail_id = serializers.IntegerField()
    location_id = serializers.IntegerField()

    def create(self, validated_data):
  
        try:
            purchase_detail = PurchaseDetail.objects.get(id=validated_data['purchase_detail_id'])
            location = Location.objects.get(id=validated_data['location_id'])

            purchase_detail.location = location
            purchase_detail.save()
            
        except  ObjectDoesNotExist :
            serializers.ValidationError({"message": "purchase_detail_id or location does not match"})
        return validated_data
