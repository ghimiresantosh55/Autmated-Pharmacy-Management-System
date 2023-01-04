'''
model serializers class for core app
'''
from django.db import models
from rest_framework import  serializers
from django.utils import timezone

# importing of models 
from .models import OrganizationRule, OrganizationSetup,  AppAccessLog,  PaymentMode
from src.user.models import User


# importing of function
from src.custom_lib.functions import current_user
from src.custom_lib.functions.fiscal_year import  get_fiscal_year_code_bs
from src.custom_lib.functions.fiscal_year import  get_fiscal_year_code_ad
from src.custom_lib.functions.fiscal_year import  get_full_fiscal_year_code_ad
from src.custom_lib.functions.fiscal_year import get_full_fiscal_year_code_bs

bs_year_code = get_fiscal_year_code_bs()
ad_year_code = get_fiscal_year_code_ad()
full_ad_year_code = get_full_fiscal_year_code_ad()
full_bs_year_code = get_full_fiscal_year_code_bs()


class OrganizationRuleSerializer(serializers.ModelSerializer):
    '''
    model serializer class for organization rule
    '''
    class Meta:
        model = OrganizationRule
        fields = "__all__"
        read_only_fields = ['created_by', 'created_date_ad', 'created_date_bs']


    def to_representation(self, instance):
        '''
        This method takes the target of the field as the value argument and return null value to blank value.
        '''
        my_fields = {'phone_no_1', 'mobile_no','pan_no','owner_name','email','website_url'}
                     
        data = super().to_representation(instance)
        for field in my_fields:
            try:
                if not data[field]:
                    data[field] = ""
            except KeyError:
                pass
        return data

    def create(self, validated_data):
        '''
        provide current time
        '''
        date_now = timezone.now()
        '''
        providing the id of current login user
        '''
        validated_data['created_by'] = current_user.get_created_by(self.context)
        '''
        after getting all validated data, it is posted in DB
        '''
        organization_rule = OrganizationRule.objects.create(**validated_data, created_date_ad=date_now)
        return organization_rule


class OrganizationSetupSerializer(serializers.ModelSerializer):
    '''
    model serializer class for organization setup
    '''

    class Meta:
        model = OrganizationSetup
        fields = "__all__"
        '''
        read_only_fields are the fields from same model. Fields mentioned here can't be editable.
        '''
        read_only_fields = ['created_by', 'created_date_ad', 'created_date_bs']

    def create(self, validated_data):
        '''
        create method for organization setup
        '''
        date_now = timezone.now()
        validated_data['created_by'] = current_user.get_created_by(self.context)
        organization_setup = OrganizationSetup.objects.create(**validated_data, created_date_ad=date_now)
        return organization_setup



class AppAccessLogSerializer(serializers.ModelSerializer):
    '''
    model serializer class for app access log
    '''
    created_by_first_name =serializers.ReadOnlyField(source="created_by.first_name", allow_null=True)
    created_by_middle_name =serializers.ReadOnlyField(source="created_by.first_name", allow_null=True)
    created_by_last_name =serializers.ReadOnlyField(source="created_by.first_name", allow_null=True)
    created_by_user_name =serializers.ReadOnlyField(source="created_by.user_name", allow_null=True)
    device_type_display= serializers.ReadOnlyField(source="get_device_type_display", allow_null=True)
    app_type_display = serializers.ReadOnlyField(source="get_app_type_display", allow_null=True)

    class Meta:
        model = AppAccessLog
        fields = "__all__"



class PaymentModeSerializer(serializers.ModelSerializer):
    '''
    model serializer class for  PaymentMode
    '''
    class Meta:
        model = PaymentMode
        fields = "__all__"
        read_only_fields = ['created_by', 'created_date_ad', 'created_date_bs']

    def create(self, validated_data):
        '''
        create method for payment mode
        '''
        date_now = timezone.now()
        validated_data['created_by'] = current_user.get_created_by(self.context)
        payment_mode = PaymentMode.objects.create(**validated_data, created_date_ad=date_now)
        return payment_mode



class CheckUniqueUserSerializer(serializers.ModelSerializer):
    '''
    model serializer class for  CheckUniqueUser
    '''
    class Meta:
        model = User
        fields = ["id","user_name","email"]
      