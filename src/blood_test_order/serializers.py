
from rest_framework import  serializers

from src.blood_test.models import TestPackage, BloodTest
from .models import BloodTestOrderMain
from django.utils import timezone
from src.custom_lib.functions import current_user
import decimal
from src.blood_test.serializers import GetBloodTestSerializer
from src.customer_order.serializers import GetCustomerSerializer,  GetDeliveryPersonSerializer
from src.customer.models import Customer
from src.user.models import User
decimal.getcontext().rounding=decimal.ROUND_HALF_UP



class  GetTestPackageSerializer(serializers.ModelSerializer):
      class Meta:
        model= TestPackage
        exclude = ['created_by', 'created_date_ad', 'created_date_bs','device_type','app_type','active','test_involved']



class  DeleteBloodTestOrderSerializer(serializers.ModelSerializer):
      class Meta:
        model= BloodTestOrderMain
        fields="__all__"


class SaveBloodTestOrderSerializer(serializers.ModelSerializer):
    delivery_status_display = serializers.ReadOnlyField(source="get_delivery_status_display", allow_null=True)
    amount_status_display = serializers.ReadOnlyField(source="get_amount_status_display", allow_null=True)


    class Meta:
        model = BloodTestOrderMain
        exclude = ['device_type','app_type','archived']
        read_only_fields = ['created_date_ad', 'created_date_bs', 'created_by','device_type','app_type' ]
    
    

    def to_representation(self, instance):
        '''
        method for get customer object
        '''
        data =  super().to_representation(instance)
        customer = Customer.objects.get(id=data["customer"])
        customer_data = GetCustomerSerializer(customer, allow_null = True)
        data["blood_test"] = GetBloodTestSerializer(instance.blood_test.all(), many=True).data
        data["test_package"] = GetTestPackageSerializer(instance.test_package.all(), many=True).data
        data['customer'] =   customer_data.data
        
        if data['delivery_person']  is not None:
            delivery_person = User.objects.get(id=data["delivery_person"])
            delivery_person_data =  GetDeliveryPersonSerializer(delivery_person, allow_null = True)
            data['delivery_person'] =  delivery_person_data.data
        return data



    def create(self, validated_data):   
        '''
        create method for Save Blood Test  order
        '''
    
        date_now = timezone.now()
        blood_tests =  validated_data.pop('blood_test')
        test_packages = validated_data.pop('test_package')
        validated_data['created_by'] = current_user.get_created_by(self.context)  
        blood_test_order_main = BloodTestOrderMain.objects.create(**validated_data, created_date_ad=date_now)
       
       
        if  blood_tests  is not None:
                for blood_test in  blood_tests:
                    blood_test_order_main.blood_test.add(blood_test)
                 
        if   test_packages is not None:
                for  test_package in  test_packages:
                    blood_test_order_main.test_package.add(test_package)


        return  blood_test_order_main



class QuickUpdateBloodTestOrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BloodTestOrderMain
        fields = ['delivery_person', 'delivery_status', 'amount_status']

   
    def update(self, instance, validated_data):
        """
        Update and return an existing  instance, given the validated data.
        """
        instance. delivery_person = validated_data.get('delivery_person', instance.delivery_person)
        instance.delivery_status = validated_data.get('delivery_status', instance.delivery_status)
        instance.amount_status = validated_data.get('amount_status', instance.amount_status)
        if instance.delivery_status==2:
           instance.archived=True
        instance.save()
        return instance




