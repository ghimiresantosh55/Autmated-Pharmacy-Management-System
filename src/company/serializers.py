'''
serializer for company app
'''
from os import error
from rest_framework import serializers
from src.custom_lib.functions import current_user
from django.utils import timezone
from django.db import IntegrityError
from rest_framework.exceptions import APIException 

# imported model here
from .models import Company
from src.supplier.models import Supplier
from src.item.models import PoPriority
from src.customer_order.serializers import  GetItemForCompanySerializer



class GetSupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        exclude = ['created_by', 'created_date_ad', 
        'created_date_bs','device_type','app_type', 'active','phone_no','pan_vat_no','address','latitude','longitude']

class savePoPrioritySerializer(serializers.ModelSerializer):
   
    name = serializers.ReadOnlyField(source="supplier.name", allow_null=True)
    class Meta:
        model = PoPriority
        exclude = ['company','app_type','device_type'] 
        read_only_fields = ['item_type_display', 'created_by', 'created_date_ad', 'created_date_bs']


    def to_representation(self, instance):
        data =  super().to_representation(instance)
        supplier = Supplier.objects.get(id=data["supplier"])
        supplier_data = GetSupplierSerializer(supplier)
        data['supplier'] =  supplier_data.data
        return data

class CompanySerializer(serializers.ModelSerializer):
    '''
    model serializer for company
    '''
    items =  GetItemForCompanySerializer(many =True, read_only=True)
    po_priorities = savePoPrioritySerializer(many =True)
    device_type_display = serializers.ReadOnlyField(source="get_device_type_display", allow_null=True)
    app_type_display = serializers.ReadOnlyField(source="get_app_type_display", allow_null=True)
    brand_image = serializers.ImageField(max_length=None, allow_empty_file=True, allow_null=True, required=False)
    
    class Meta:
        model = Company
        fields = "__all__"
        '''
        read only fields for company,
        '''
        read_only_fields = ['created_by', 'created_date_ad', 'created_date_bs','device_type','app_type', 'device_type_display','app_type_display']


    def create(self, validated_data):
        '''
        create method for company
        '''
        po_priorities = validated_data.pop('po_priorities')
        date_now = timezone.now()
        validated_data['created_by'] = current_user.get_created_by(self.context)  
        company = Company.objects.create(**validated_data, created_date_ad=date_now)

        for po_priority in po_priorities:
            if PoPriority.objects.filter(supplier=po_priority['supplier'] ,company=company.id).exists():
                raise serializers.ValidationError('supplier and priority value should be unique together')

            if PoPriority.objects.filter(company=company.id, priority= po_priority['priority']).exists():
                raise serializers.ValidationError('supplier and priority value should be unique together')
            try:
                PoPriority.objects.create(**po_priority, company = company, created_by = validated_data['created_by'],
                                created_date_ad=date_now)
            except IntegrityError as exc:
                raise APIException(detail=exc)
                
        return company
    
   