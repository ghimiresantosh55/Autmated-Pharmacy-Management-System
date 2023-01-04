from rest_framework import serializers
from src.custom_lib.functions import current_user
from django.utils import timezone
# imported model here
from .models import Supplier, SupplierContact


# serializer for supplier

class SupplierContactSerializer(serializers.ModelSerializer):
    '''
    model serializer for supplier contact serializer
    '''
    class Meta:
        model = SupplierContact
        fields = "__all__"
        read_only_fields = ['created_by', 'created_date_ad', 'created_date_bs','device_type','app_type']

    def create(self, validated_data):
        '''
        create method for supplier contact
        '''
        date_now = timezone.now()
        validated_data['created_by'] = current_user.get_created_by(self.context)
        supplier_contact = SupplierContact.objects.create(**validated_data, created_date_ad=date_now)
        return supplier_contact



class SaveSupplierContactSerializer(serializers.ModelSerializer):
    '''
    save supplier contact serializer for get
    '''
    class Meta:
        model = SupplierContact
        exclude = ["supplier"]
        read_only_fields = ['created_by', 'created_date_ad', 'created_date_bs','device_type','app_type'] 



class SupplierSerializer(serializers.ModelSerializer):
    '''
    serializer for save supplier
    '''
    supplier_contacts =  SaveSupplierContactSerializer(many =True)
    class Meta:
        model = Supplier
        fields = "__all__"
        read_only_fields = ['created_by', 'created_date_ad', 'created_date_bs','device_type','app_type']


    def create(self, validated_data):
        '''
        create method for supplier module
        '''
        supplier_contacts = validated_data.pop('supplier_contacts')
        date_now = timezone.now()
        validated_data['created_by'] = current_user.get_created_by(self.context)
        supplier = Supplier.objects.create(**validated_data,  created_date_ad=date_now)
        for supplier_contact in supplier_contacts:
            SupplierContact.objects.create(**supplier_contact, supplier = supplier, created_by =validated_data['created_by'],
                                      created_date_ad=date_now)
        return supplier

  
