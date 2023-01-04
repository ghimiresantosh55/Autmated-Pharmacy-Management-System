from rest_framework import serializers
from src.customer.models import Customer
from src.sale.models import SaleDetail, SaleMain
from src.customer_order.serializers import GetUserSerializer

class SaleDetailSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.brand_name', default="")
    unit_name = serializers.CharField(source='item_unit.name', default="")
    class Meta:
        model = SaleDetail
        exclude = ['sale_main']


class SaleMainReportSerializer(serializers.ModelSerializer):

    sale_details = SaleDetailSerializer(many=True)
    sale_type_display = serializers.CharField(source='get_sale_type_display')
    customer_first_name = serializers.CharField(source='customer.first_name')
    customer_last_name = serializers.CharField(source='customer.last_name')
    created_by_first_name = serializers.CharField(source='created_by.first_name', default="")
    created_by_middle_name = serializers.CharField(source='created_by.middle_name', default="")
    created_by_last_name = serializers.CharField(source='created_by.last_name', default="")
    device_type_display= serializers.ReadOnlyField(source="get_device_type_display", allow_null=True, default="")
    app_type_display = serializers.ReadOnlyField(source="get_app_type_display", allow_null=True, default="")
     
  
    class Meta:
        model = SaleMain
        fields = "__all__"


class SaleMainSummarySerializer(serializers.ModelSerializer):
    sale_type_display = serializers.CharField(source='get_sale_type_display')
    customer_first_name = serializers.CharField(source='customer.first_name', default="")
    customer_last_name = serializers.CharField(source='customer.last_name', default="")
    created_by_first_name = serializers.CharField(source='created_by.first_name', default="")
    created_by_middle_name = serializers.CharField(source='created_by.middle_name',  default="")
    created_by_last_name = serializers.CharField(source='created_by.last_name',  default="")
    device_type_display= serializers.ReadOnlyField(source="get_device_type_display", allow_null=True , default="")
    app_type_display = serializers.ReadOnlyField(source="get_app_type_display", allow_null=True ,default="")
     
   
    class Meta:
        model = SaleMain
        fields = "__all__"


class CustomerReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id", "first_name", "last_name"]


class SaleGetDataSerializer(serializers.Serializer):
    sale_types = serializers.SerializerMethodField()
    filter_fields = serializers.ListField(child=serializers.CharField())
    ordering_fields = serializers.ListField(child=serializers.CharField())
    search_fields = serializers.ListField(child=serializers.CharField())
    customers = CustomerReportSerializer(many=True)
    users= GetUserSerializer(many = True)

    def get_sale_types(self, instance):
        sale_types =  dict(SaleMain.SALE_TYPE)
        data = []
     
        for key, value in sale_types.items():
            data.append({"key": key, "value": value})
        
        return data


