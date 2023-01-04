from rest_framework import serializers
from decimal import Decimal
from src.purchase.models import PurchaseMain, PurchaseDetail
from src.supplier.models import Supplier
from src.customer_order.serializers import GetUserSerializer


class PurchaseDetailSerializer(serializers.ModelSerializer):
    item_name = serializers.ReadOnlyField(source='item.brand_name', allow_null=True)
    unit_name = serializers.CharField(source='item_unit.name',allow_null=True)
   
    class Meta:
        model = PurchaseDetail
        exclude = ['purchase_main']

  
class PurchaseMainReportSerializer(serializers.ModelSerializer):
    purchase_details =  PurchaseDetailSerializer(many=True)
    purchase_type_display = serializers.ReadOnlyField(source='get_purchase_type_display', allow_null=True ,default="")
    supplier_name = serializers.ReadOnlyField(source='supplier.name', default="")
    created_by_first_name = serializers.CharField(source='created_by.first_name', default="")
    created_by_middle_name = serializers.CharField(source='created_by.middle_name' ,default="")
    created_by_last_name = serializers.CharField(source='created_by.last_name', default="")
    device_type_display= serializers.ReadOnlyField(source="get_device_type_display", allow_null=True, default="")
    app_type_display = serializers.ReadOnlyField(source="get_app_type_display", allow_null=True, default="")
     
  
    class Meta:
        model = PurchaseMain
        fields = "__all__"

   

class SummaryPurchaseMainSerializer(serializers.ModelSerializer):
    purchase_type_display = serializers.ReadOnlyField(source='get_purchase_type_display', allow_null=True, default="")
    supplier_name = serializers.ReadOnlyField(source='supplier.name', default="")
    created_by_first_name = serializers.CharField(source='created_by.first_name', default="")
    created_by_middle_name = serializers.CharField(source='created_by.middle_name', default="")
    created_by_last_name = serializers.CharField(source='created_by.last_name', default="")
    device_type_display= serializers.ReadOnlyField(source="get_device_type_display", allow_null=True, default="")
    app_type_display = serializers.ReadOnlyField(source="get_app_type_display", allow_null=True, default="")
     
    class Meta:
        model = PurchaseMain
        fields = "__all__"

   
   
class SupplierReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ["id", "name", "address","phone_no"]

class PurchaseGetDataSerializer(serializers.Serializer):
    purchase_types = serializers.SerializerMethodField()
    filter_fields = serializers.ListField(child=serializers.CharField())
    ordering_fields = serializers.ListField(child=serializers.CharField())
    search_fields = serializers.ListField(child=serializers.CharField())
    suppliers = SupplierReportSerializer(many=True)
    users= GetUserSerializer(many = True)


    def get_purchase_types(self, instance):
        purchase_types =  dict(PurchaseMain.PURCHASE_TYPE)
        data = []
     
        for key, value in purchase_types.items():
            data.append({"key": key, "value": value})
        
        return data
