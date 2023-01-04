from rest_framework import serializers
from src.purchase_order.models import PurchaseOrderMain, PurchaseOrderDetail
from src.supplier.models import Supplier
from src.customer_order.serializers import GetUserSerializer

class PurchaseOrderDetailSerializer(serializers.ModelSerializer):
    available_display =  serializers.ReadOnlyField(source='get_available_display', allow_null=True, default="")
    item_name = serializers.ReadOnlyField(source='item.brand_name', allow_null=True, default="")
    unit_name = serializers.CharField(source='item_unit.name',allow_null=True, default="")
   
    class Meta:
        model = PurchaseOrderDetail
        exclude = ['purchase_order_main']

  

class PurchaseOrderMainReportSerializer(serializers.ModelSerializer):
    purchase_order_details =  PurchaseOrderDetailSerializer(many=True)
    customer_order_order_no = serializers.ReadOnlyField(source='customer_order_main.order_no', allow_null=True, default="")
    purchase_order_type_display = serializers.ReadOnlyField(source='get_purchase_order_type_display', allow_null=True, default="")
    supplier_name = serializers.ReadOnlyField(source='supplier.name', default="")
    created_by_first_name = serializers.CharField(source='created_by.first_name', default="")
    created_by_middle_name = serializers.CharField(source='created_by.middle_name', default="")
    created_by_last_name = serializers.CharField(source='created_by.last_name', default="")
    device_type_display= serializers.ReadOnlyField(source="get_device_type_display", allow_null=True, default="")
    app_type_display = serializers.ReadOnlyField(source="get_app_type_display", allow_null=True, default="")
     
  
    class Meta:
        model = PurchaseOrderMain
        fields = "__all__"

   

class SummaryPurchaseOrderMainSerializer(serializers.ModelSerializer):
    customer_order_order_no = serializers.ReadOnlyField(source='customer_order_main.order_no', allow_null=True, default="")
    purchase_order_type_display = serializers.ReadOnlyField(source='get_purchase_order_type_display', allow_null=True, default="")
    supplier_name = serializers.ReadOnlyField(source='supplier.name', default="")
    created_by_first_name = serializers.CharField(source='created_by.first_name', default="")
    created_by_middle_name = serializers.CharField(source='created_by.middle_name', default="")
    created_by_last_name = serializers.CharField(source='created_by.last_name', default="")
    device_type_display= serializers.ReadOnlyField(source="get_device_type_display", allow_null=True, default="")
    app_type_display = serializers.ReadOnlyField(source="get_app_type_display", allow_null=True, default="")
     
  
    class Meta:
        model = PurchaseOrderMain
        fields = "__all__"



class SupplierReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ["id", "name", "address","phone_no"]

class PurchaseOrderGetDataSerializer(serializers.Serializer):
    purchase_order_types = serializers.SerializerMethodField()
    filter_fields = serializers.ListField(child=serializers.CharField())
    ordering_fields = serializers.ListField(child=serializers.CharField())
    search_fields = serializers.ListField(child=serializers.CharField())
    suppliers = SupplierReportSerializer(many=True)
    users= GetUserSerializer(many = True)

    def get_purchase_order_types(self, instance):
        order_types =  dict(PurchaseOrderMain.PURCHASE_ORDER_TYPE)
        data = []
     
        for key, value in order_types.items():
            data.append({"key": key, "value": value})
        
        return data

