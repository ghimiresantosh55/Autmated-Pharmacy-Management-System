from rest_framework import serializers
from src.customer.models import Customer
from src.customer_order.models import OrderDetail, OrderMain
from src.user.models import User
from src.customer_order.serializers import GetUserSerializer

class CustomerOrderDetailSerializer(serializers.ModelSerializer):
    '''
    serializer for get  customer order  detail data
    '''
    item_name = serializers.CharField(source='item.brand_name', default="")
    unit_name = serializers.CharField(source='item_unit.name', default="")
    class Meta:
        model = OrderDetail
        exclude = ['order']


class CustomerOrderMainReportSerializer(serializers.ModelSerializer):
    '''
    serializer for get customer order main report data
    '''
    order_details = CustomerOrderDetailSerializer(many=True)
    delivery_status_name = serializers.CharField(source='get_delivery_status_display')
    customer_first_name = serializers.CharField(source='customer.first_name')
    customer_last_name = serializers.CharField(source='customer.last_name', default="")
    amount_status_name = serializers.CharField(source='get_amount_status_display')
    created_by_first_name = serializers.CharField(source='created_by.first_name')
    created_by_middle_name = serializers.CharField(source='created_by.middle_name')
    created_by_last_name = serializers.CharField(source='created_by.last_name')
    delivery_person_first_name = serializers.CharField(source='delivery_person.first_name', default="")
    delivery_person_middle_name = serializers.CharField(source='delivery_person.middle_name', default="")
    delivery_person_last_name = serializers.CharField(source='delivery_person.last_name', default="")

    class Meta:
        model = OrderMain
        fields = "__all__"


class CustomerOrderMainSummarySerializer(serializers.ModelSerializer):
    '''
    serializer for get customer order main summary data
    '''
    delivery_status_name = serializers.CharField(source='get_delivery_status_display')
    customer_first_name = serializers.CharField(source='customer.first_name')
    customer_last_name = serializers.CharField(source='customer.last_name')
    amount_status_name = serializers.CharField(source='get_amount_status_display')
    created_by_first_name = serializers.CharField(source='created_by.first_name')
    created_by_middle_name = serializers.CharField(source='created_by.middle_name')
    created_by_last_name = serializers.CharField(source='created_by.last_name')
    delivery_person_first_name = serializers.CharField(source='delivery_person.first_name', default="")
    delivery_person_middle_name = serializers.CharField(source='delivery_person.middle_name', default="")
    delivery_person_last_name = serializers.CharField(source='delivery_person.last_name', default="")
    class Meta:
        model = OrderMain
        fields = "__all__"

class CustomerReportSerializer(serializers.ModelSerializer):
    '''
    serializer for get customer report data
    '''
    class Meta:
        model = Customer
        fields = ["id","first_name", "last_name"]
        

class CustomerOrderGetDataSerializer(serializers.Serializer):
    '''
    serializer for  customer order get data
    '''
    delivery_status_types = serializers.SerializerMethodField()
    filter_fields = serializers.ListField(child=serializers.CharField())
    ordering_fields = serializers.ListField(child=serializers.CharField())
    search_fields = serializers.ListField(child=serializers.CharField())
    users= GetUserSerializer(many = True)
    customers = CustomerReportSerializer(many=True)

    def get_delivery_status_types(self, instance):
        status_types =  dict(OrderMain.DELIVERY_STATUS_TYPE)
        data = []
     
        for key, value in status_types.items():
            data.append({"key": key, "value": value})
        
        return data

        


