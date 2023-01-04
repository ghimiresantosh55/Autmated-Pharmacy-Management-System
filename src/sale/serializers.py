from rest_framework import  serializers, status
from src.customer_order.models import OrderDetail, OrderMain
from src.purchase.models import PurchaseMain
from .models import SaleMain, SaleDetail, SalePaymentDetail
from django.utils import timezone
from src.custom_lib.functions import current_user
from decimal import Decimal
from src.customer.models import Customer
from src.item.models import Item, ItemUnit
from src.item.serializers import GetItemUnitSerializer
from . import save_sale_service
import decimal
from src.custom_lib.functions.stock import get_sale_return_qty, get_sale_remaining_qty




class UpdatePurchaseMainSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseMain
        fields = '__all__'


class SaleMainSerializer(serializers.ModelSerializer):
     
    class Meta:
        model = SaleMain
        fields = '__all__'


class GetCustomerSerializer(serializers.ModelSerializer):
    '''
    model serializer for get customer data
    '''
    class Meta:
        model = Customer
        exclude = [ 'created_date_ad', 
        'created_date_bs','home_address','office_address','home_google_location','office_google_location','alt_phone_no']


class GetItemSerializer(serializers.ModelSerializer):
    '''
    model serializer for get item data
    '''
    class Meta:
        model = Item
        exclude = ['created_date_ad','created_date_bs','active','created_by','device_type','app_type','item_details','price',\
        'discount_rate','image','verified','purchase_qty','free_qty','item_unit','medicine_form','company','product_category','generic_name']


class GetRefSaleMainForSaleReturnSerializer(serializers.ModelSerializer):

    class Meta:
        model = SaleMain
        exclude = ['created_date_ad','created_date_bs','created_by','device_type','app_type','sale_type','pay_type',\
        'customer','total_amount','ref_sale_main','remarks','active','ref_customer_order_main']


class SaveSaleDetailSerializer(serializers.ModelSerializer):
    '''
    Model serializer for save sale  detail for get
    '''
    item_name = serializers.ReadOnlyField(source='item.brand_name', allow_null=True, default="")
    created_by_user_name = serializers.ReadOnlyField(source='created_by.user_name', allow_null=True, default="")
    class Meta:
        model = SaleDetail
        exclude = ['sale_main']
        read_only_fields = ['created_date_ad', 'created_date_bs', 'created_by','device_type','app_type', 'device_type_display','app_type_display']



class ListSaleDetailSerializer(serializers.ModelSerializer):
    '''
    Model serializer for sale detail list
    '''
    item_name = serializers.ReadOnlyField(source='item.brand_name', allow_null=True, default="")
    created_by_user_name = serializers.ReadOnlyField(source='created_by.user_name', allow_null=True, default="")

    class Meta:
        model = SaleDetail
        exclude= ['sale_main']

    def to_representation(self, instance):
        '''
        method of get objects
        '''
        data =  super().to_representation(instance)
        if data['item_unit'] is not None:
            item_unit = ItemUnit.objects.get(id=data["item_unit"])
            item_unit_data = GetItemUnitSerializer(item_unit)
            data['item_unit'] =  item_unit_data.data
        item = Item.objects.get(id=data["item"])
        item_data = GetItemSerializer(item)
        data['item'] =  item_data.data
        return data
    

  
class ListSaleMainSerializer(serializers.ModelSerializer):
    '''
    model serializer for listing sale detail data
    '''
    sale_details = ListSaleDetailSerializer(many=True)
    customer_first_name = serializers.ReadOnlyField(source='customer.first_name')
    customer_last_name = serializers.ReadOnlyField(source='customer.last_name', default="")
    sale_type_display =  serializers.ReadOnlyField(source="get_sale_type_display", allow_null=True)
    pay_type_display = serializers.ReadOnlyField(source="get_pay_type_display", allow_null=True)

    class Meta:
        model = SaleMain
        fields = '__all__'

    def to_representation(self, instance):
        '''
        method to get objects 
        '''
        data =  super().to_representation(instance)
        customer = Customer.objects.get(id=data["customer"])
        customer_data = GetCustomerSerializer(customer)
        data['customer'] =  customer_data.data
        return data
       


class SaveSaleSerializer(serializers.ModelSerializer):
    '''
    model serializer for save sale
    '''
    sale_details = SaveSaleDetailSerializer(many = True)
    customer_first_name = serializers.ReadOnlyField(source='customer.first_name')
    customer_last_name = serializers.ReadOnlyField(source='customer.last_name', default="")
    device_type_display = serializers.ReadOnlyField(source="get_device_type_display", allow_null=True, default="")
    app_type_display = serializers.ReadOnlyField(source="get_app_type_display", allow_null=True, default="")
    customer_order_delivery_status= serializers.ReadOnlyField(source="ref_customer_order_main.delivery_status", allow_null=True, default="")
    delivery_status_display= serializers.ReadOnlyField(source="ref_customer_order_main.get_delivery_status_display", default="")
    
    class Meta:
        model = SaleMain
        fields = '__all__'
        read_only_fields = ['created_date_ad', 'created_date_bs', 'created_by','device_type','app_type', 'device_type_display','app_type_display']


    def to_representation(self, instance):
        '''
        method for get supplier object
        '''
        data =  super().to_representation(instance)
        if data['customer']  is not None:
            customer = Customer.objects.get(id=data["customer"])
            customer_data = GetCustomerSerializer(customer)
            data['customer'] =  customer_data.data
        return data


    def create(self, validated_data):
        '''
        method to create save sale
        '''
        sale_details  = save_sale_service.update_purchase_for_sale(validated_data.pop('sale_details'))
        # sale_details  = validated_data.pop('sale_details')
        # print(sale_details, "this is sale details")
        date_now = timezone.now()
        validated_data['created_by'] = current_user.get_created_by(self.context)
        sale_main = SaleMain.objects.create(**validated_data, created_date_ad=date_now)

        # update customer order 
        if sale_main.ref_customer_order_main:
            customer_order = sale_main.ref_customer_order_main
            customer_order.delivery_status = 3 #billed
            customer_order.save()  

        for sale_detail in sale_details:
            SaleDetail.objects.create(**sale_detail, sale_main = sale_main, created_by =validated_data['created_by'],
                                        created_date_ad=date_now)
        return sale_main



    def validate(self, data):
            '''
            validation method for save sale
            '''
            decimal.getcontext().rounding=decimal.ROUND_HALF_UP
            quantize_places = Decimal(10) ** -2
            total_amount = Decimal('0.00')
            sale_details = data['sale_details']
            
            for sale in sale_details:
                sale_detail = {}
                key_values = zip(sale .keys(), sale.values())
                for key, values in key_values:
                    sale_detail[key] = values
                    # print(values)
                
                if  sale_detail['amount'] <= 0 or  sale_detail['qty'] <=0:
                    raise serializers.ValidationError({
                        f'item {sale_detail["item"].brand_name}': 'values in fields, amount, net_amount and quantity  cannot be less than'
                                                                ' or equals to 0'})
                if  sale_detail['discount_rate'] < 0 or  sale_detail['net_amount'] < 0 or  sale_detail['sub_total'] < 0:
                    raise serializers.ValidationError({
                        f'item {sale_detail["item"].brand_name}': 'values in field, discount rate, net_amount, sub_total cannot be less than 0'})

                # validation for discount amount
                discount_rate = (sale_detail['discount_amount'] *
                                 Decimal('100')) / (sale_detail['amount'] *
                                                    sale_detail['qty'])
                discount_rate = discount_rate.quantize(quantize_places)

                #validation for sub_total
                sub_total =  sale_detail['amount'] *  sale_detail['qty']
                sub_total = sub_total.quantize(quantize_places)

                net_amount =  net_amount = ((sale_detail['amount'] * sale_detail['qty'])-((sale_detail['amount']*sale_detail['qty']*sale_detail['discount_rate'])/Decimal('100')))
                net_amount = net_amount.quantize(quantize_places)

                if  sub_total!=  sale_detail['sub_total']:
                    raise serializers.ValidationError({f'item { sale_detail["item"].brand_name}':
                        f'sub_total calculation not valid : should be {sub_total }'})


                if net_amount != sale_detail['net_amount']:
                     raise serializers.ValidationError({f'item {sale_detail["item"].brand_name}':
                         'net_amount calculation not valid : should be {}'.format(net_amount)})


                total_amount = net_amount + total_amount
                #validation for total_amount
            if  total_amount != data['total_amount']:
                
                    raise serializers.ValidationError(
                    'total_amount calculation {} not valid: should be {}'.format(data['total_amount'], total_amount))

            if data['ref_customer_order_main'] is not None:
                customer_order_id=data['ref_customer_order_main'].id
                customer_order_data= OrderMain.objects.get(id= customer_order_id)
                customer_order_delivery_status=customer_order_data.delivery_status
               
                if customer_order_delivery_status==2 or customer_order_delivery_status==3 or customer_order_delivery_status==4 or \
                        customer_order_delivery_status==5 or customer_order_delivery_status==6:
                            raise serializers.ValidationError("Only pending order are accepted to make bill.")

            # if data['ref_customer_order_detail'] is not None:
            #         customer_order_id=data['ref_customer_order_detail'].id
            #         customer_order_data= OrderDetail.objects.get(id= customer_order_id)
            #         customer_order_informed=customer_order_data.order_details.informed

            # if  customer_order_informed==True:
            #        raise serializers.ValidationError("you can not make bill of informed")
            return data 



class SaveSaleForReturnSerializer(serializers.ModelSerializer):
    '''
    model serializer for save sale for return
    '''
    sale_details = SaveSaleDetailSerializer(many = True)
    sale_type_display= serializers.ReadOnlyField(source="get_sale_type_display", allow_null=True, default="")
    device_type_display = serializers.ReadOnlyField(source="get_device_type_display", allow_null=True, default="")
    app_type_display = serializers.ReadOnlyField(source="get_app_type_display", allow_null=True, default="")
    
    class Meta:
        model = SaleMain
        fields = '__all__'
        read_only_fields = ['created_date_ad', 'created_date_bs', 'created_by','device_type','app_type', 'device_type_display','app_type_display']


    def to_representation(self, instance):
        '''
        method for get supplier object
        '''
        data =  super().to_representation(instance)
        if data['customer']  is not None:
            customer = Customer.objects.get(id=data["customer"])
            customer_data = GetCustomerSerializer(customer)
            data['customer'] =  customer_data.data

        if data['ref_sale_main']  is not None:
            ref_sale_main= SaleMain.objects.get(id=data["ref_sale_main"])
            ref_sale_main_data= GetRefSaleMainForSaleReturnSerializer(ref_sale_main)
            data['ref_sale_main'] =  ref_sale_main_data.data

        return data


    def create(self, validated_data):

        '''
        method to create save sale
        '''
        self.create_validate(validated_data)
        sale_details  = validated_data.pop('sale_details')
        if not sale_details:
            serializers.ValidationError("Please provide at least one sale detail")
        date_now = timezone.now()
        validated_data['created_by'] = current_user.get_created_by(self.context)
        sale_main = SaleMain.objects.create(**validated_data,  created_date_ad=date_now)
        for sale_detail in sale_details:
            SaleDetail.objects.create(**sale_detail, sale_main = sale_main, created_by =validated_data['created_by'],
                                        created_date_ad=date_now)
        return sale_main



    def create_validate(self, data):
            '''
            validation method for save sale
            '''
            decimal.getcontext().rounding=decimal.ROUND_HALF_UP
            quantize_places = Decimal(10) ** -2
            total_amount = Decimal('0.00')
            sale_details = data['sale_details']
        
            for sale in sale_details:
                sale_detail = {}
                key_values = zip(sale .keys(), sale.values())
                for key, values in key_values:
                    sale_detail[key] = values
                    # print(values)
                
                if  sale_detail['amount'] <= 0 or  sale_detail['qty'] <=0:
                    raise serializers.ValidationError({
                        f'item {sale_detail["item"].brand_name}': 'values in fields, amount, net_amount and quantity  cannot be less than'
                                                                ' or equals to 0'})
                if  sale_detail['discount_rate'] < 0 or  sale_detail['net_amount'] < 0 or  sale_detail['sub_total'] < 0:
                    raise serializers.ValidationError({
                        f'item {sale_detail["item"].brand_name}': 'values in field, discount rate, net_amount, sub_total cannot be less than 0'})

                # validation for discount amount
                discount_rate = (sale_detail['discount_amount'] *
                                 Decimal('100')) / (sale_detail['amount'] *
                                                    sale_detail['qty'])
                discount_rate = discount_rate.quantize(quantize_places)

                #validation for sub_total
                sub_total =  sale_detail['amount'] *  sale_detail['qty']
                sub_total = sub_total.quantize(quantize_places)

                net_amount = (sub_total - sale_detail['discount_amount'])
                net_amount = net_amount.quantize(quantize_places)

                if  sub_total!=  sale_detail['sub_total']:
                    raise serializers.ValidationError({f'item { sale_detail["item"].brand_name}':
                        f'sub_total calculation not valid : should be {sub_total }'})


                if net_amount != sale_detail['net_amount']:
                     raise serializers.ValidationError({f'item {sale_detail["item"].brand_name}':
                         'net_amount calculation not valid : should be {}'.format(net_amount)})

                total_amount = net_amount + total_amount
                #validation for total_amount
            if  total_amount != data['total_amount']:
                
                    raise serializers.ValidationError(
                    'total_amount calculation {} not valid: should be {}'.format(data['total_amount'], total_amount)
                )
            return data 
            

class SalePaymentDetailSerializer(serializers.ModelSerializer):
    '''
    Model serializer class for sale payment detail
    '''
    sale_no = serializers.ReadOnlyField(source='sale_master.sale_no', allow_null=True)
    payment_mode_name = serializers.ReadOnlyField(source='payment_mode.name', allow_null=True)

    class Meta:
        model = SalePaymentDetail
        fields = "__all__"
        read_only_fields = ['created_by', 'created_date_ad', 'created_date_bs']



class SaleDetailForSaleReturnSerializer(serializers.ModelSerializer):
    '''
    model serializer class for sale detail for sale return
    '''
    item_name = serializers.ReadOnlyField(source='item.brand_name')
    item_code_name = serializers.ReadOnlyField(source='item.code')
    unit_name = serializers.ReadOnlyField(source='item.item_unit.name')
    unit_short_form = serializers.ReadOnlyField(source='item.item_unit.short_form')
    return_qty = serializers.SerializerMethodField()
    remaining_qty = serializers.SerializerMethodField()

    class Meta:
        model = SaleDetail
        exclude = ['created_date_ad', 'created_date_bs', 'ref_sale_detail', 'created_by','device_type','app_type']

    def get_return_qty(self, sale):
        '''
        method for get return quantity
        '''
        sale_id = sale.id
        qty = get_sale_return_qty(sale_id)
        return qty


    def get_remaining_qty(self, sale):
        '''
        Method for get remaining quantity
        '''
        sale_id = sale.id
        qty = get_sale_remaining_qty(sale_id)
        return qty
