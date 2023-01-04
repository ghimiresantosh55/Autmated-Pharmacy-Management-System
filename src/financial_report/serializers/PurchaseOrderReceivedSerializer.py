
from rest_framework import serializers
from src.purchase_order.models import PurchaseOrderReceivedMain, PurchaseOrderReceivedDetail
from src.supplier.models import Supplier
from src.customer_order.serializers import GetUserSerializer


class PurchaseOrderReceivedDetailSerializer(serializers.ModelSerializer):
    '''
    serializer for purchase order received detail data
    '''
    item_name = serializers.ReadOnlyField(source='item.brand_name', allow_null=True, default="")
    unit_name = serializers.CharField(source='item_unit.name',allow_null=True, default="")
   
    class Meta:
        model = PurchaseOrderReceivedDetail
        exclude = ['purchase_order_received_main']

  

class PurchaseOrderReceivedMainReportSerializer(serializers.ModelSerializer):
    '''
    serializer for purchase order received main report data
    '''
    purchase_order_received_details =  PurchaseOrderReceivedDetailSerializer(many=True)
    purchase_order_received_type_display = serializers.ReadOnlyField(source='get_purchase_order_received_type_display', allow_null=True, default="")
    supplier_name = serializers.ReadOnlyField(source='supplier.name', default="")
    created_by_first_name = serializers.CharField(source='created_by.first_name', default="")
    created_by_middle_name = serializers.CharField(source='created_by.middle_name', default="")
    created_by_last_name = serializers.CharField(source='created_by.last_name', default="")
    device_type_display= serializers.ReadOnlyField(source="get_device_type_display", allow_null=True, default="")
    app_type_display = serializers.ReadOnlyField(source="get_app_type_display", allow_null=True, default="")
     
    class Meta:
        model = PurchaseOrderReceivedMain
        fields = "__all__"


class SummaryPurchaseOrderReceivedMainSerializer(serializers.ModelSerializer):
    '''
    serializer for summary purchase order received data
    '''
    purchase_order_received_type_display = serializers.ReadOnlyField(source='get_purchase_order_received_type_display', allow_null=True, default="")
    supplier_name = serializers.ReadOnlyField(source='supplier.name', default="")
    created_by_first_name = serializers.CharField(source='created_by.first_name', default="")
    created_by_middle_name = serializers.CharField(source='created_by.middle_name', default="")
    created_by_last_name = serializers.CharField(source='created_by.last_name', default="")
    device_type_display= serializers.ReadOnlyField(source="get_device_type_display", allow_null=True, default="")
    app_type_display = serializers.ReadOnlyField(source="get_app_type_display", allow_null=True, default="")
     
  
    class Meta:
        model = PurchaseOrderReceivedMain
        fields = "__all__"



class SupplierReportSerializer(serializers.ModelSerializer):
    '''
    serializer for supplier report data
    '''
    class Meta:
        model = Supplier
        fields = ["id", "name", "address","phone_no"]

class PurchaseOrderReceivedGetDataSerializer(serializers.Serializer):
    '''
    serializer for purchase order received get data
    '''
    purchase_order_received_types = serializers.SerializerMethodField()
    filter_fields = serializers.ListField(child=serializers.CharField())
    ordering_fields = serializers.ListField(child=serializers.CharField())
    search_fields = serializers.ListField(child=serializers.CharField())
    suppliers = SupplierReportSerializer(many=True)
    users= GetUserSerializer(many = True)

    def get_purchase_order_received_types(self, instance):
        purchase_order_received_types =  dict(PurchaseOrderReceivedMain.PURCHASE_ORDER_RECEIVED_TYPE)
        data = []
     
        for key, value in purchase_order_received_types.items():
            data.append({"key": key, "value": value})
        
        return data

    