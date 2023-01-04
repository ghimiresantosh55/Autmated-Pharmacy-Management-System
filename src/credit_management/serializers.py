from re import T
from rest_framework import serializers
from src.item.models import Item
from src.credit_management.models import CreditClearance, CreditPaymentDetail
from src.customer.models import Customer
from src.sale.models import SaleDetail
from src.custom_lib.functions.current_user import get_created_by
from src.sale.models import SaleMain
from django.utils import timezone
from src.custom_lib.functions import current_user
from decimal import Decimal
from src.sale.serializers import SaveSaleDetailSerializer
from django.db import connection
import itertools
from django.db.models import F


class GetCustomerForCreditSerializer(serializers.ModelSerializer):
    '''
    Serializer for get customer data whose have credit
    '''
    class Meta:
        model = Customer
        exclude = ['home_address', 'created_date_ad', 'created_date_bs', 'home_google_location', 'user', 'client_no',
                   'alt_phone_no', 'office_google_location']


class CreditPaymentMainSerializer(serializers.ModelSerializer):
    '''
    Model Serializer for Credit payment main
    '''
    created_by_user_name = serializers.ReadOnlyField(source='created_by.user_name', allow_null=True)
    sale_no = serializers.ReadOnlyField(source='sale_main.sale_no', allow_null=True)
    payment_type_display = serializers.ReadOnlyField(source='get_payment_type_display', allow_null=True)

    class Meta:
        model = CreditClearance
        fields = "__all__"
        read_only_fields = ['payment_type_display']


class CreditPaymentDetailSerializer(serializers.ModelSerializer):
    '''
    Model serializer for credit payment detail
    '''

    class Meta:
        model = CreditPaymentDetail
        fields = '__all__'
        read_only_fields = ('created_date_ad', 'created_date_bs', 'created_by')


"""_________________________________save credit payment details_________________________________________________"""


class SaveCreditPaymentDetailSerializer(serializers.ModelSerializer):
    ''''
    Model serializer for save credit payment detail
    '''
    payment_mode_name = serializers.ReadOnlyField(source='payment_mode.name')

    class Meta:
        model = CreditPaymentDetail
        exclude = ['credit_clearance', 'app_type', 'device_type']
        read_only_fields = ('created_date_ad', 'created_date_bs', 'created_by')


class SaveCreditClearanceSerializer(serializers.ModelSerializer):
    ''''
    Model serializer class for credit clearance
    '''
    credit_payment_details = SaveCreditPaymentDetailSerializer(many=True)
    sale_no = serializers.ReadOnlyField(source='sale_main.sale_no', allow_null=True)

    class Meta:
        model = CreditClearance
        fields = '__all__'
        read_only_fields = ('created_date_ad', 'created_date_bs', 'created_by')

    def create(self, validated_data):
        date_now = timezone.now()
        credit_payment_details = validated_data.pop('credit_payment_details')

        validated_data['created_by'] = get_created_by(self.context)

        credit_clearance = CreditClearance.objects.create(**validated_data, created_date_ad=date_now)
        for credit_payment_detail in credit_payment_details:
            CreditPaymentDetail.objects.create(**credit_payment_detail, credit_clearance=credit_clearance,
                                               created_by=validated_data['created_by'], created_date_ad=date_now)

        return credit_clearance


"""_______________________ serializer for Credit Sale Report _______________________________________________"""


class SaleCreditSerializer(serializers.ModelSerializer):
    '''
    Model serializer for sale credit
    '''
    sale_id = serializers.ReadOnlyField(source='id')
    created_by_user_name = serializers.ReadOnlyField(source='created_by.user_name', allow_null=True)
    customer_first_name = serializers.ReadOnlyField(source='customer.first_name', allow_null=True)
    customer_last_name = serializers.ReadOnlyField(source='customer.last_name', allow_null=True)
    total_amount = serializers.ReadOnlyField()
    paid_amount = serializers.SerializerMethodField()
    due_amount = serializers.SerializerMethodField()
    total_amount = serializers.SerializerMethodField()
    class Meta:
        model = SaleMain
        fields = ['sale_id', 'sale_no', 'customer', 'customer_first_name',
                  'customer_last_name', 'total_amount',
                  'paid_amount', 'due_amount', 'created_date_ad', 'created_date_bs',
                  'created_by', 'created_by_user_name', 'remarks']


    def get_paid_amount(self, instance):
        '''
        Method for get paid amount
        '''
        paid_amount = sum(CreditClearance.objects.filter(sale_main=instance.id, payment_type=1)
                          .values_list('total_amount', flat=True))
        refund_amount = sum(CreditClearance.objects.filter(
            sale_main=instance, payment_type=2).values_list('total_amount', flat=True))
        return paid_amount - refund_amount


    def get_due_amount(self, instance):
        '''
        Method for get due amount
        '''
        paid_amount = self.get_paid_amount(instance)
        due_amount = self.get_total_amount(instance) - paid_amount
        return due_amount


    def get_total_amount(self, instance):
        total_sale_amount = instance.total_amount
        total_sale_return_amount = sum(SaleMain.objects.filter(
            ref_sale_main=instance.id).values_list('total_amount', flat=True))
        return total_sale_amount-total_sale_return_amount

class SaleCreditCustomerWiseSerializer(serializers.ModelSerializer):

    '''
    model serializer for sale credit customer wise
    '''
    paid_amount = serializers.SerializerMethodField()
    due_amount = serializers.SerializerMethodField()
    total_credit_amount = serializers.SerializerMethodField()
   
  
    class Meta:
        model = Customer

        fields = ['id', 'first_name',
                  'last_name', 'paid_amount', 'total_credit_amount',
                  'due_amount', 'created_date_ad', 'created_date_bs' ]


    def get_total_credit_amount(self, instance):
        '''
        Method for get total credit amount
        '''
        total_credit_amount = sum(SaleMain.objects.filter(customer=instance.id, pay_type=2, ref_sale_main__isnull=True)
                                  .values_list('total_amount', flat=True))
        return_credit_sale_amount = sum(SaleMain.objects.filter(
            customer=instance.id, pay_type=2, ref_sale_main__isnull=False
        ).values_list('total_amount', flat=True))
        return total_credit_amount - return_credit_sale_amount


    def get_paid_amount(self, instance):
        '''
        Method for get paid amount
        '''
        paid_amount = sum(CreditClearance.objects.filter(sale_main__customer=instance.id, payment_type=1)
                          .values_list('total_amount', flat=True))
        refund_amount = sum(CreditClearance.objects.filter(
            payment_type=2, sale_main__customer=instance.id).values_list('total_amount', flat=True))
        return paid_amount - refund_amount

    def get_due_amount(self, instance):
        '''
        method for get due amount
        '''
        paid_amount = self.get_paid_amount(instance)
        total_credit_amount = self.get_total_credit_amount(instance)
        due_amount = total_credit_amount - paid_amount
        return due_amount
    
    # def get_paid_date_ad(self, instance):
    #     paid_date_ad =(CreditClearance.objects.filter(sale_main__customer=instance.id).values('created_date_ad'))
    #     return  paid_date_ad
  

    # def get_paid_date_bs(self, instance):
    #     paid_date_bs = (CreditClearance.objects.filter(sale_main__customer = instance.id).values_list('created_date_bs',flat=True))
    #     return  paid_date_bs
  
      
class ReceiptNoCustomerWiseSerializer(serializers.ModelSerializer):
    '''
    model serializer for get receipt data customerwise
    '''
    receipt_data = serializers.SerializerMethodField()

    class Meta:
        model = Customer

        fields = ['id', 'receipt_data']

    def get_receipt_data(self, instance):
        '''
        method for get receipt no. , totalamount and verified date and verified by
        '''
        receipt_data = CreditClearance.objects.filter(sale_main__customer=instance.id).values('id',
                                                                                              'receipt_no').annotate(
            verified_by=F('created_by__user_name'), verified_date_bs=F('created_date_bs'),
            paid_amount=F('total_amount'))
        return receipt_data
