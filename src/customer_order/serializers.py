
from pickle import FALSE
from wsgiref.validate import validator
from attr import validate
from rest_framework import  serializers
from .models import OrderMain, OrderDetail
from django.utils import timezone
from src.custom_lib.functions import current_user
from decimal import Decimal
from src.item.models import Item, ItemUnit
from src.customer.models import Customer
from src.user.models import User
from src.sale.models import SaleDetail, SaleMain, SalePaymentDetail
from src.credit_management.models import CreditPaymentDetail, CreditClearance
from src.credit_management.reciept_unique_id_generator import get_receipt_no
import decimal
from rest_framework import status
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
decimal.getcontext().rounding=decimal.ROUND_HALF_UP


class GetItemSerializer(serializers.ModelSerializer):
    '''
    serializer for get item data
    '''
    class Meta:
        model = Item
        exclude = ['created_date_ad', 'created_date_bs', 'created_by','device_type','app_type','active']


class GetItemForCompanySerializer(serializers.ModelSerializer):
    '''
    serializer for get item data for company
    '''
    class Meta:
        model = Item
        exclude = ['created_date_ad', 'created_date_bs', 'created_by','device_type','app_type','active','generic_name','company',\
            'product_category','item_details','medicine_form','image','price','discount_rate','verified','purchase_qty','free_qty','item_unit']


class GetItemUnitSerializer(serializers.ModelSerializer):
    '''
    serializer for get item  unit data
    '''
    class Meta:
        model = ItemUnit
        exclude = ['created_date_ad', 'created_date_bs', 'created_by','device_type','app_type','active']


class GetCustomerSerializer(serializers.ModelSerializer):
    '''
    serializer for get data of customer
    '''
    class Meta:
        model = Customer
        exclude = ['created_date_ad', 'created_date_bs','office_address','user' ,'alt_phone_no','home_google_location', 'office_google_location','client_no']
  

class GetDeliveryPersonSerializer(serializers.ModelSerializer):
    '''
    serializer for get data of delivery person
    '''
    class Meta:
        model = User
        exclude = ['created_date_ad', 'middle_name','created_date_bs','user_type', 'photo','mobile_no', 'address','gender','active','is_staff',
        'birth_date','group','groups','user_permissions','created_by','is_superuser','password','last_login']


class GetUserSerializer(serializers.ModelSerializer):
    '''
    serializer for get user data
    '''
    
    class Meta:
        model = User
        fields = ["id","user_name","email","first_name","middle_name","last_name","created_date_ad","created_date_bs"]


class GetUserForCustomerSerializer(serializers.ModelSerializer):
    '''
    serializer for get user data for customer
    '''
    class Meta:
        model = User
        fields = ["id","user_name"]

class DeleteOrderDetailSerializer(serializers.ModelSerializer):
    '''
    Model serializer for delete order details
    '''
    item_name = serializers.ReadOnlyField(source="item.brand_name", allow_null=True)
    item_unit_name = serializers.ReadOnlyField(source="item_unit.name", allow_null=True)
    ws_unit =  serializers.ReadOnlyField(source="item.ws_unit", allow_null=True)
    class Meta:
        model =OrderDetail
        fields =  "__all__"   


class OrderDetailSerializer(serializers.ModelSerializer):
    '''
    Model serializer for order detail for get
    '''
    class Meta:
        model = OrderDetail
        exclude=['archived','cancelled']
        read_only_fields = ['created_date_ad', 'created_date_bs', 'created_by']


    def create(self, validated_data):
        '''
        create method for order detail
        '''
        date_now = timezone.now()
        validated_data['created_by'] = current_user.get_created_by(self.context)
        order_detail = OrderDetail.objects.create(**validated_data, created_date_ad=date_now)
        return order_detail
    
    def to_representation(self, instance):
        '''
        method for get objects
        '''
        data =  super().to_representation(instance)
        # data = OrderDetail.objects.filter(archived=False, id=data['id'])
        if data['item_unit']  is not None:
            item_unit = ItemUnit.objects.get(id=data["item_unit"])
            item_unit_data = GetItemUnitSerializer(item_unit)
            data['item_unit'] =  item_unit_data.data
        return data



class SaveOrderDetailSerializer(serializers.ModelSerializer):
    '''
    Model serializer for get Save Order Detail 
    '''
    item_name = serializers.ReadOnlyField(source="item.brand_name", allow_null=True)
    item_unit_name = serializers.ReadOnlyField(source="item_unit.name", allow_null=True)
    ws_unit =  serializers.ReadOnlyField(source="item.ws_unit", allow_null=True)
    
    class Meta:
      model = OrderDetail
      exclude = ['order','device_type','app_type','archived', 'cancelled']
      read_only_fields = ['created_date_ad', 'created_date_bs', 'created_by']


    def to_representation(self, instance):
        '''
        method for get objects
        '''
        data =  super().to_representation(instance)
        # data = OrderDetail.objects.filter(archived=False, id=data['id'])
        if data['item_unit']  is not None:
            item_unit = ItemUnit.objects.get(id=data["item_unit"])
            item_unit_data = GetItemUnitSerializer(item_unit)
            data['item_unit'] =  item_unit_data.data
        return data



class SaveCustomerOrderSerializer(serializers.ModelSerializer):
    '''
    Model serializer for save customer order
    '''
    order_details = SaveOrderDetailSerializer(many=True)
    delivery_status_display = serializers.ReadOnlyField(source="get_delivery_status_display", allow_null=True)
    amount_status_display = serializers.ReadOnlyField(source="get_amount_status_display", allow_null=True)
    # total_amount = serializers.ReadOnlyField()
    total_amount_credit = serializers.SerializerMethodField()
    paid_amount = serializers.SerializerMethodField()
    due_amount = serializers.SerializerMethodField()
    sale_no = serializers.SerializerMethodField()

    class Meta:
        model = OrderMain
        exclude = ['device_type','app_type']
        read_only_fields = ['created_date_ad', 'created_date_bs', 'created_by','device_type','app_type', \
        'acknowledge_order', 'amount_status', 'delivery_status']


    def get_sale_no(self, instance):

        "Method of get sale main"
        try:
            sale_main =  SaleMain.objects.get(ref_customer_order_main = instance.id)
            sale_no = sale_main.sale_no
            return sale_no
        except ObjectDoesNotExist:
            return None


    def get_total_amount_credit(self, instance):
        total_amount_credit = sum(SaleMain.objects.filter(ref_customer_order_main=instance.id).values_list("total_amount", flat = True))
        return total_amount_credit


    def get_paid_amount(self, instance):
        '''
        Method for get paid amount
        '''
        paid_amount = sum(CreditClearance.objects.filter(sale_main__ref_customer_order_main = instance.id)
                          .values_list('total_amount', flat=True))
        return paid_amount


    def get_due_amount(self, instance):
        '''
        Method for get due amount
        '''
        paid_amount = self.get_paid_amount(instance)
        total_amount_credit = self. get_total_amount_credit(instance)
        due_amount = total_amount_credit - paid_amount
        return due_amount


    def to_representation(self, instance):
        '''
        method for get customer object
        '''
        data =  super().to_representation(instance)
        customer = Customer.objects.get(id=data["customer"])
        customer_data = GetCustomerSerializer(customer, allow_null = True)
        data['customer'] =   customer_data.data
        
        if data['delivery_person']  is not None:
            delivery_person = User.objects.get(id=data["delivery_person"])
            delivery_person_data =  GetDeliveryPersonSerializer(delivery_person, allow_null = True)
            data['delivery_person'] =  delivery_person_data.data
        return data


    def create(self, validated_data):   
        '''
        create method for Save customer order
        '''
        # print(validated_data, "customer order valid data")
        self.create_validate(validated_data)
        order_details = validated_data.pop('order_details')
        date_now = timezone.now()
        if not order_details:
            raise serializers.ValidationError("Please provide at least one order detail")
        validated_data['created_by'] = current_user.get_created_by(self.context)  
        order_main = OrderMain.objects.create(**validated_data, created_date_ad=date_now)
        for order_detail in order_details:
              OrderDetail.objects.create(**order_detail, order = order_main, created_by = validated_data['created_by'],
                                created_date_ad=date_now)        
        return order_main


    def create_validate(self, data):
        # print(data)
        decimal.getcontext().rounding=decimal.ROUND_HALF_UP
        quantize_places = Decimal(10) ** -2
        total_amount = Decimal('0.00')
        net_amount = Decimal('0.00')
        customer_order_details = data['order_details']
      
        for customer_order in customer_order_details:
            customer_order_detail = {}
            key_values = zip(customer_order.keys(), customer_order.values())
            for key, values in key_values:
                customer_order_detail[key] = values
             
            
            if customer_order_detail['amount'] <= 0 or customer_order_detail['qty'] <=0:
                raise serializers.ValidationError({
                    f'item {customer_order_detail["item"].brand_name}': 'values in fields, amount and  quantity  cannot be less than'
                                                            ' or equals to 0'})

            if customer_order_detail['discount_rate'] < 0 or customer_order_detail['net_amount'] < 0 or  customer_order_detail['sub_total'] < 0:
                    raise serializers.ValidationError({
                        f'item {customer_order_detail["item"].brand_name}': 'values in field, discount rate, net_amount, sub_total cannot be less than 0'})

            
            discount_rate = (customer_order_detail['discount_amount'] *
                                 Decimal('100')) / (customer_order_detail['amount'] *
                                                    customer_order_detail['qty'])
            discount_rate = discount_rate.quantize(quantize_places)
            
            
            #validation for sub_total   
            sub_total = customer_order_detail['amount'] * customer_order_detail['qty']
            sub_total = sub_total.quantize(quantize_places)
           
            net_amount = (sub_total-(customer_order_detail['amount']*customer_order_detail['qty']*customer_order_detail['discount_rate'])/Decimal('100'))
            # print(net_amount,"before quantize")
            net_amount = net_amount.quantize(quantize_places)
        
            # print(net_amount,"after quantize")

            if  sub_total!= customer_order_detail['sub_total']:
                raise serializers.ValidationError({f'item {customer_order_detail["item"].brand_name}':
                    f'sub_total calculation not valid : should be {sub_total }'})

            if net_amount != customer_order_detail['net_amount']:
                raise serializers.ValidationError({f'item {customer_order_detail["item"].brand_name}':
                    'net_amount calculation not valid : should be {}'.format(net_amount)})

            total_amount = net_amount + total_amount
            #validation for total_amount
        if  total_amount != data['total_amount']:
              
                raise serializers.ValidationError(
                  'total_amount calculation {} not valid: should be {}'.format(data['total_amount'], total_amount)
            )
        return data 



    # def partial_update_validate(self, instance, data):
    #     order_main = instance
    #     quantize_places = Decimal(10) ** -2
    #     total_amount = order_main.total_amount
    #     customer_order_details = data['order_details']
      
    
    #     for customer_order in customer_order_details:
    #         customer_order_detail = {}
    #         key_values = zip(customer_order.keys(), customer_order.values())
    #         for key, values in key_values:
    #             customer_order_detail[key] = values
    #             # print(values)
            
    #         if customer_order_detail['amount'] <= 0 or customer_order_detail['qty'] <=0:
    #             raise serializers.ValidationError({
    #                 f'item {customer_order_detail["item"].brand_name}': 'values in fields, amount and  quantity  cannot be less than'
    #                                                         ' or equals to 0'})


    #         #validation for sub_total
    #         sub_total = customer_order_detail['amount'] * customer_order_detail['qty']
    #         sub_total = sub_total.quantize(quantize_places)
    #         if  sub_total!= customer_order_detail['sub_total']:
    #             raise serializers.ValidationError({f'item {customer_order_detail["item"].brand_name}':
    #                 f'sub_total calculation not valid : should be {sub_total }'})

    #         total_amount = total_amount + sub_total
    #         #validation for total_amount
    #     if  total_amount != data['total_amount']:
    #         raise serializers.ValidationError(
    #             f'total_amount calculation {data["total_amount"]} not valid: should be {total_amount}'
    #             )
    #     return instance 


    
class UpdateOrderMainSerializer(serializers.ModelSerializer):
    '''
    model serializer for update order main
    '''
    class Meta:
        model = OrderMain
        fields = ['acknowledge_order', 'delivery_person', 'delivery_status', 'amount_status']

   
    def update(self, instance, validated_data):
        """
        Update and return an existing  instance, given the validated data.
        """
        instance.acknowledge_order = validated_data.get('acknowledge_order', instance.acknowledge_order)
        instance. delivery_person = validated_data.get('delivery_person', instance.delivery_person)
        instance.delivery_status = validated_data.get('delivery_status', instance.delivery_status)
        instance.amount_status = validated_data.get('amount_status', instance.amount_status)
        if instance.delivery_status==2:
            order_details = OrderDetail.objects.filter(order=instance.id)
            for order_detail in order_details:
                order_detail.cancelled=True
                order_detail.save()
        instance.save()
        return instance


class BulkUpdateOrderMainSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderMain
        fields = ['id', 'acknowledge_order', 'delivery_person', 'delivery_status']




class SaveOrderDetailForDispatchSerializer(serializers.ModelSerializer):  
    '''
    model serializer class for save order detail for dispatch
    '''
    item_name = serializers.ReadOnlyField(source="item.brand_name", allow_null=True)
    item_unit_name = serializers.ReadOnlyField(source="item_unit.name", allow_null=True)
    
    class Meta:
      model = SaleDetail
      exclude = ['sale_main','ref_sale_detail','ref_purchase_detail','ref_customer_order_detail']
      read_only_fields = ['created_date_ad', 'created_date_bs', 'created_by']



class CustomerOrderDispatchViewSerializer(serializers.ModelSerializer):
    '''
    Model serializer class for customer order dispatch
    '''
    customer_first_name = serializers.ReadOnlyField(source="customer.first_name", allow_null=True)
    customer_middle_name = serializers.ReadOnlyField(source="customer.middle_name", allow_null=True,default = "")
    customer_last_name = serializers.ReadOnlyField(source="customer.last_name", allow_null=True, default = "")
    customer_phone_no = serializers.ReadOnlyField(source="customer.phone_no", allow_null=True, default = "")
    delivery_person_user_name=  serializers.ReadOnlyField(source="delivery_person.user_name", allow_null=True, default = "")
    delivery_person_first_name = serializers.ReadOnlyField(source="delivery_person.first_name", allow_null=True, default = "")
    delivery_person_last_name = serializers.ReadOnlyField(source="delivery_person.last_name", allow_null=True, default = "")
    delivery_status_display = serializers.ReadOnlyField(source="get_delivery_status_display", allow_null=True)
    amount_status_display = serializers.ReadOnlyField(source="get_amount_status_display", allow_null=True)
    order_details = SaveOrderDetailForDispatchSerializer(many=True)

    class Meta:
        model = OrderMain
        fields = '__all__'

 
class SaveCreditPaymentDetailOnDispatchSerializer(serializers.ModelSerializer):
    '''
    Model serializer for save sale payment on dispatch serializer
    '''
    class Meta:
        model =  CreditPaymentDetail
        exclude= ['credit_clearance']


class SaveCreditClearanceSerializer(serializers.ModelSerializer):
    '''
    Model serializer class for save credit clearance
    '''

    receipt_no = serializers.CharField(max_length = 20, required=False, allow_blank = True)
    credit_payment_details = SaveCreditPaymentDetailOnDispatchSerializer(many= True)
    class Meta:
        model = CreditClearance
        fields= "__all__"



class CustomerOrderDispatchCreateSerializer(serializers.ModelSerializer):
    '''
    model serializer for customer order dispatch for create
    '''
    customer_first_name = serializers.ReadOnlyField(source="customer.first_name", allow_null=True)
    customer_middle_name = serializers.ReadOnlyField(source="customer.middle_name", allow_null=True,default = "")
    customer_last_name = serializers.ReadOnlyField(source="customer.last_name", allow_null=True, default = "")
    customer_phone_no = serializers.ReadOnlyField(source="customer.phone_no", allow_null=True, default = "")
    delivery_person_first_name = serializers.ReadOnlyField(source="delivery_person.first_name", allow_null=True, default = "")
    delivery_person_last_name = serializers.ReadOnlyField(source="delivery_person.last_name", allow_null=True, default = "")
    delivery_status_display = serializers.ReadOnlyField(source="get_delivery_status_display", allow_null=True)
    amount_status_display = serializers.ReadOnlyField(source="get_amount_status_display", allow_null=True)
    credit_clearance =  SaveCreditClearanceSerializer(required = False)
  
    class Meta:
        model = OrderMain
        fields = "__all__"
        read_only_fields = ['order_no','customer','delivery_person','amount_status','total_amount','order_location','google_location',\
          'acknowledge_order' ,'delivery_date_ad','remarks' ,'order_details','app_type','device_type', 'created_date_ad', \
              'created_date_bs', 'created_by','delivery_status']

    
    def update(self, instance, validated_data):
        '''
        Update method for customer order dispatch
        '''

        if instance.delivery_status==5:
            instance.delivery_status=6
            instance.save() 

        else:
            raise serializers.ValidationError("Only Dispatched status will be updated to Done")
                   
        created_by = current_user.get_created_by(self.context)

        try:
            sale = SaleMain.objects.get(ref_customer_order_main = instance.id)
        except ObjectDoesNotExist:
            raise serializers.ValidationError({'message': 'ref customer order to sale does not exist'})
        
        if validated_data['credit_clearance']['receipt_no']== "":
            validated_data['credit_clearance']['receipt_no'] = get_receipt_no()
        
        validated_data['sale_main'] = sale
        credit_clearance_data = validated_data['credit_clearance'].copy()

        credit_payment_details = credit_clearance_data.pop('credit_payment_details') 
        
        if credit_clearance_data:
            credit_clear = CreditClearance.objects.create(**credit_clearance_data, sale_main = sale, 
                                    created_by =  created_by, created_date_ad = timezone.now())

            for payment_data in credit_payment_details:
                CreditPaymentDetail.objects.create(**payment_data, credit_clearance = credit_clear,  
                                        created_date_ad = timezone.now(), created_by=created_by)
        return instance
        

class AmountOrderMainSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    # amount_status = serializers.ChoiceField(choices= OrderMain.AMOUNT_STATUS)
  
class AmountStatusBulkUpdateSerializer(serializers.Serializer):
    '''
    Serializer class for bulk  update of amount
    '''
    order_mains =  AmountOrderMainSerializer(many = True)
  
    # class Meta:
    #     model = OrderMain
    #     fields = ["id", "amount_status", "order_mains"]
                   
    def create(self, validated_data):
        '''
        Create method for update and insert amount to bulk update amount
        '''
        validated_datas = validated_data.copy()

        for data in validated_data["order_mains"]:
            created_by = current_user.get_created_by(self.context)
        
            try:
                sale_main =  SaleMain.objects.get(ref_customer_order_main = data['id'])
            except ObjectDoesNotExist:
                raise serializers.ValidationError({'message': 'ref customer order to sale does not exist'})

        
            paid_amount = sum(CreditClearance.objects.filter(sale_main__ref_customer_order_main = data['id'])
                            .values_list('total_amount', flat=True))

            total_amount_credit = sum(SaleMain.objects.filter(ref_customer_order_main = data['id']).values_list("total_amount",  flat = True))

            due_amount = (total_amount_credit - paid_amount)

            credit_clearance = {}
            credit_clearance ['receipt_no'] = get_receipt_no()
            credit_clearance['sale_main'] = sale_main
            credit_clearance['payment_type'] = 1
            credit_clearance['remarks'] = ""
            credit_clearance['total_amount'] = due_amount
            credit_clearance['ref_credit_clearance'] = None
    
                                                    
            credit_clear = CreditClearance.objects.create(**credit_clearance,
                                        created_by =  created_by, created_date_ad = timezone.now())
            
        return  validated_datas
   

  

   

       