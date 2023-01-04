# importing of function
from src.custom_lib.functions import current_user
from rest_framework import serializers
from src.party_payment.models import  PartyPayment,PartyPaymentDetail
from src.custom_lib.functions.current_user import get_created_by
from src.purchase.models import PurchaseMain
from src.supplier.models import Supplier
from django.utils import timezone
from src.custom_lib.functions import current_user
from django.utils import timezone
from src.custom_lib.functions.current_user import get_created_by
from rest_framework.response import Response
from rest_framework import serializers,  status
from django.db.models import F


class PartyPaymentMasterSerializer(serializers.ModelSerializer):
    '''
    model serializer class for Partypayment master
    '''
    created_by_user_name = serializers.ReadOnlyField(source='created_by.user_name', allow_null=True)
    payment_type_display= serializers.ReadOnlyField(source='get_payment_type_display', allow_null=True)
    purchase_no = serializers.ReadOnlyField(source='purchase_master.purchase_no', allow_null=True)
  
    class Meta:
        model = PartyPayment
        fields = "__all__"


class PartyPaymentDetailSerializer(serializers.ModelSerializer):
    '''
    Model serializer for party payment detail
    '''
    created_by_user_name = serializers.ReadOnlyField(source='created_by.user_name', allow_null=True)
    payment_mode_name = serializers.ReadOnlyField(source='payment_mode.name', allow_null=True)
    

    class Meta:
        model = PartyPaymentDetail
        fields = '__all__'
        read_only_fields = ('created_date_ad', 'created_date_bs', 'created_by')


"""_________________________________save credit payment details_________________________________________________"""


class SavePartyPaymentDetailSerializer(serializers.ModelSerializer):
    '''
    Model serializer for party payment detail saving
    '''
    payment_mode_name = serializers.ReadOnlyField(source='payment_mode.name')

    class Meta:
        model = PartyPaymentDetail
        exclude = ['party_payment']
        read_only_fields = ('created_date_ad', 'created_date_bs', 'created_by')


class SavePartyPaymentSerializer(serializers.ModelSerializer):
    '''
    Model serializer class for save party payment
    '''
    party_payment_details = SavePartyPaymentDetailSerializer(many=True)
   
    class Meta:
        model = PartyPayment
        fields = '__all__'
        read_only_fields = ( 'created_date_ad', 'created_date_bs', 'created_by')


    def create(self, validated_data):
        date_now = timezone.now()
        party_payment_details = validated_data.pop('party_payment_details')

        validated_data['created_by'] = get_created_by(self.context)

        party_clearance = PartyPayment.objects.create(**validated_data, created_date_ad=date_now)
        for party_payment_detail in party_payment_details:
            PartyPaymentDetail.objects.create(**party_payment_detail, party_payment=party_clearance,
                                              created_by=validated_data['created_by'], created_date_ad=date_now)

        return party_clearance


"""_______________________ serializer for Credit Sale Report _______________________________________________"""


class PurchaseCreditSerializer(serializers.ModelSerializer):
    purchase_id = serializers.ReadOnlyField(source='id')
    purchase_number = serializers.ReadOnlyField(source='purchase_no', allow_null=True)
    created_by_user_name = serializers.ReadOnlyField(source='created_by.user_name', allow_null=True)
    supplier_name = serializers.ReadOnlyField(source='supplier.name', allow_null=True)
    paid_amount = serializers.SerializerMethodField()
    due_amount = serializers.SerializerMethodField()
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = PurchaseMain
        fields = ['purchase_id','purchase_number', 'supplier_name', 'created_by_user_name',
                 'total_amount',
                  'paid_amount', 'due_amount', 'purchase_no', 'supplier', 'created_date_ad', 'created_date_bs',
                  'created_by', 'remarks']

    def get_paid_amount(self, instance):
        paid_amount = sum(PartyPayment.objects.filter(purchase_main=instance.id, payment_type=1)
                          .values_list('total_amount', flat=True))
        
        refund_amount = sum(PartyPayment.objects.filter(purchase_main=instance.id, payment_type=2).values_list('total_amount', flat=True))
        return paid_amount - refund_amount


    def get_due_amount(self, instance):
        paid_amount = self.get_paid_amount(instance)
        due_amount = self.get_total_amount(instance) - paid_amount
        return due_amount
    

    def get_total_amount(self, instance):
        purchase_total_amount = instance.total_amount
        purchase_return_amount = sum(PurchaseMain.objects.filter(ref_purchase=instance.id).values_list('total_amount', flat=True))
        
        return purchase_total_amount-purchase_return_amount


class PurchaseCreditSupplierWiseSerializer(serializers.ModelSerializer):
    '''
    model serializer for purchase credit
    '''
    total_party_payment_amount = serializers.SerializerMethodField()
    paid_amount = serializers.SerializerMethodField()
    due_amount = serializers.SerializerMethodField()

    class Meta:
        model = Supplier
        fields = ['id' , 'name',
                  'total_party_payment_amount',
                  'paid_amount', 'due_amount',  'created_date_ad', 'created_date_bs',
                 ]


    def get_total_party_payment_amount(self, instance): 
        '''
        method for get total party payment amount
        '''
        total_credit_amount = sum(PurchaseMain.objects.filter(supplier=instance.id, pay_type =2, ref_purchase__isnull=True)
                          .values_list('total_amount', flat=True))
        total_return_credit_amount = sum(PurchaseMain.objects.filter(supplier=instance.id,pay_type=2,ref_purchase__isnull=False).values_list('total_amount', flat=True))
        return total_credit_amount - total_return_credit_amount
  

    def get_paid_amount(self, instance):
        '''
        method for get paid amount
        '''
        paid_amount = sum(PartyPayment.objects.filter(purchase_main__supplier=instance.id,payment_type=1)
                          .values_list('total_amount', flat=True))
        refund_amount = sum(PartyPayment.objects.filter(purchase_main__supplier=instance.id,payment_type=2).values_list('total_amount',flat=True))
        return paid_amount - refund_amount


    def get_due_amount(self, instance):
        '''
        method for get due amount
        '''
        paid_amount = self.get_paid_amount(instance)
        total_party_payment_amount=self.get_total_party_payment_amount(instance)
        due_amount = total_party_payment_amount - paid_amount
        return due_amount


class ReceiptNoSupplierWiseSerializer(serializers.ModelSerializer):
    '''
    model serializer for get receipt data customerwise
    '''
    receipt_data = serializers.SerializerMethodField()
   
    class Meta:
        model = Supplier

        fields = ['id',  'receipt_data']
                   
                   

    def get_receipt_data(self, instance): 
        
        receipt_data = PartyPayment.objects.filter(purchase_main__supplier=instance.id).values('id','receipt_no').annotate(verified_by =F('created_by__user_name'), verified_date_bs=F('created_date_bs'), paid_amount=F('total_amount'))
        return receipt_data




