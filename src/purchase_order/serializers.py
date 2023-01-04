from rest_framework import serializers

from src.purchase.models import PurchaseMain, PurchaseDetail
from .models import PurchaseOrderDetail, PurchaseOrderMain, PurchaseOrderReceivedMain, PurchaseOrderReceivedDetail
from src.supplier.models import Supplier
from src.company.serializers import GetSupplierSerializer
from src.custom_lib.functions import current_user
from decimal import Decimal
from django.utils import timezone
from src.user.models import User
from src.customer_order.serializers import GetUserSerializer
from src.item.serializers import GetItemSerializer
from src.item.models import Item
from decimal import Decimal
import decimal
from src.purchase.serializers import SavePurchaseDetailSerializer
from decimal import Decimal
from rest_framework import serializers
from src.customer_order.models import OrderDetail, OrderMain
from src.purchase_order.models import PurchaseOrderMain, PurchaseOrderDetail
from src.custom_lib.functions import custom_seq_generator
from src.item.models import Item, PoPriority
from src.supplier.models import Supplier
from django.utils import timezone
from src.custom_lib.functions import current_user
from django.core.exceptions import ObjectDoesNotExist
from src.custom_lib.functions.stock import get_remaining_qty_of_item, get_purchase_order_unverified_qty, get_pending_customer_order_qty
from src.purchase.purchase_unique_id_generator import generate_purchase_no
quantize_places = Decimal(10) ** -2



class ListPurchaseOrderDetailSerializer(serializers.ModelSerializer):
    '''
    model serializer for Listing Purchase order detail data
    '''
    item_unit_name =  serializers.ReadOnlyField(source="item_unit.name", allow_null=True, default = "")
    item_price = serializers.ReadOnlyField(source="item.price", allow_null=True, default = "")
    item_name =  serializers.ReadOnlyField(source="item.brand_name", allow_null=True, default = "")
    class Meta:
        model = PurchaseOrderDetail
        fields = "__all__"


class ListPurchaseOrderMainSerializer(serializers.ModelSerializer):
    '''
    model serializer for listing of purchase order main and related purchase order detail data
    '''
    purchase_order_details = ListPurchaseOrderDetailSerializer(many=True)
    purchase_order_type_display = serializers.ReadOnlyField(source='get_purchase_order_type_display', allow_null=True)
    supplier_name = serializers.ReadOnlyField(source='supplier.name', allow_null=True)
    assigned_to_first_name = serializers.ReadOnlyField(source='assigned_to.first_name', allow_null=True)
    assigned_to_middle_name = serializers.ReadOnlyField(source='assigned_to.middle_name', allow_null=True)
    assigned_to_last_name = serializers.ReadOnlyField(source='assigned_to.last_name', allow_null=True)
    class Meta:
        model = PurchaseOrderMain
        fields = "__all__"


    def to_representation(self, instance):
        data =  super().to_representation(instance)
        if data['supplier'] is not None:
            supplier = Supplier.objects.get(id=data["supplier"])
            supplier_data = GetSupplierSerializer(supplier)
            data['supplier'] = supplier_data.data

        if data['assigned_to'] is not None:
            assigned_to = User.objects.get(id=data["assigned_to"])
            assigned_to_data = GetUserSerializer(assigned_to)
            data['assigned_to'] =  assigned_to_data.data

        return data



class ListPurchaseOrderReceivedDetailSerializer(serializers.ModelSerializer):
    '''
    model serializer for listing purchase order received detail data
    '''
    item_price = serializers.ReadOnlyField(source="item.price", allow_null=True)
    item_name =  serializers.ReadOnlyField(source="item.brand_name", allow_null=True)
    class Meta:
        model = PurchaseOrderReceivedDetail
        exclude=['archived']


    def to_representation(self, instance):
    
        data = super().to_representation(instance)
        if data['item']  is not None:
            item = Item.objects.get(id=data["item"])
            item_data = GetItemSerializer(item)
            data['item'] =  item_data.data
        return data



class ListPurchaseOrderReceivedMainSerializer(serializers.ModelSerializer):
    '''
    model serializer for listing purchase order received main data
    '''
    purchase_order_received_details = ListPurchaseOrderReceivedDetailSerializer(many=True)
    purchase_order_received_type_display = serializers.ReadOnlyField(source='get_purchase_order_received_type_display', allow_null=True)
    supplier_name = serializers.ReadOnlyField(source='supplier.name', allow_null=True)
    status_type_is_verified  = serializers.SerializerMethodField()
    class Meta:
        model = PurchaseOrderReceivedMain
        fields = "__all__"

    
    def get_status_type_is_verified(self, instance):
        if PurchaseOrderReceivedMain.objects.filter(ref_purchase_order_received_main=instance.id).exists():
            return True
        else:
            return False

                          

class SavePurchaseOrderDetailSerializer(serializers.ModelSerializer):
    '''
    model serializer for save purchase detail data in save purchase model
    '''
    class Meta:
        model = PurchaseOrderDetail
        exclude = ['purchase_order_main']
        read_only_fields = ['created_by', 'created_date_ad', 'created_date_bs','device_type','app_type']

        def to_representation(self, instance):
            my_fields = {'ref_purchase_order_detail', 'ref_purchase_detail'}
            data = super().to_representation(instance)
            for field in my_fields:
                try:
                    if not data[field]:
                        data[field] = ""
                except KeyError:
                 pass
            return data



class SavePurchaseOrderReceivedDetailSerializer(serializers.ModelSerializer):
    '''
    model serializer for save purchase detail data in save purchase model
    '''
    item_name= serializers.ReadOnlyField(source='item.brand_name', allow_null=True)

    class Meta:
        model = PurchaseOrderReceivedDetail
        exclude = ['purchase_order_received_main','archived']
        read_only_fields = ['created_by', 'created_date_ad', 'created_date_bs','device_type','app_type']
    def create(self, validated_data):
        print(validated_data,"this is validated data")
        pass


class SavePurchaseOrderMainSerializer(serializers.ModelSerializer):
    '''
    model serializer for save purchase order main
    '''
    purchase_order_details = SavePurchaseOrderDetailSerializer(many=True)
    purchase_order_type_display = serializers.ReadOnlyField(source='get_purchase_order_type_display', allow_null=True)
    supplier_name = serializers.ReadOnlyField(source='supplier.name', allow_null=True)
    class Meta:
        model = PurchaseOrderMain
        fields = "__all__"
        read_only_fields = ['created_by', 'created_date_ad', 'created_date_bs','device_type','app_type']


    def to_representation(self, instance):
        '''
        method for get empty string
        '''
        my_fields = {'ref_purchase', 'ref_purchase_order_main'}
                   
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
        create method for save purchase order main
        '''
        # purchase_main
        self.create_validate(validated_data)
        validated_data['created_by'] = current_user.get_created_by(self.context)
        date_now = timezone.now()
        purchase_order_details = validated_data.pop('purchase_order_details')

        purchase_order_main = PurchaseOrderMain.objects.create(**validated_data, created_date_ad=date_now)
       
         

        for purchase_order_detail in purchase_order_details:
            PurchaseOrderDetail.objects.create(** purchase_order_detail, purchase_order_main=purchase_order_main,
                                          created_by=validated_data['created_by'], created_date_ad=date_now)
        return purchase_order_main


    def create_validate(self, data):
        '''
        validation method for create purchase order main
        '''
        decimal.getcontext().rounding=decimal.ROUND_HALF_UP
        quantize_places = Decimal(10) ** -2
        total_amount = Decimal('0.00')
        net_amount = Decimal('0.00')
        purchase_order_details = data['purchase_order_details']
      

        for purchase_order in purchase_order_details:
            purchase_order_detail = {}
            key_values = zip(purchase_order.keys(), purchase_order.values())
            for key, values in key_values:
                purchase_order_detail[key] = values
              
            
            if  purchase_order_detail['amount'] <= 0 or   purchase_order_detail ['qty'] <=0:
                raise serializers.ValidationError({
                    f'item { purchase_order_detail ["item"].brand_name}': 'values in fields, amount and  quantity  cannot be less than'
                                                            ' or equals to 0'})

            if  purchase_order_detail['discount_rate'] < 0 or purchase_order_detail['net_amount'] < 0 or  purchase_order_detail['sub_total'] < 0:
                    raise serializers.ValidationError({
                        f'item {purchase_order_detail["item"].brand_name}': 'values in field, discount rate, net_amount, sub_total cannot be less than 0'})

             # validation for discount amount
            discount_rate = (purchase_order_detail['discount_amount'] *
                                 Decimal('100')) / (purchase_order_detail['amount'] *
                                                    purchase_order_detail['qty'])
            discount_rate = discount_rate.quantize(quantize_places)


            #validation for sub_total
            sub_total =  purchase_order_detail['amount']*purchase_order_detail ['qty']
            sub_total = sub_total.quantize(quantize_places)

            net_amount =  ((purchase_order_detail['amount'] * purchase_order_detail['qty'])-((purchase_order_detail['amount']*['qty']*purchase_order_detail['discount_rate'])/Decimal('100')))
            net_amount = net_amount.quantize(quantize_places)

            if  sub_total!= purchase_order_detail['sub_total']:
                raise serializers.ValidationError({f'item {purchase_order_detail ["item"].brand_name}':
                    f'sub_total calculation not valid : should be {sub_total }'})

            if net_amount != purchase_order_detail['net_amount']:
                raise serializers.ValidationError({f'item {purchase_order_detail["item"].brand_name}':
                    'net_amount calculation not valid : should be {}'.format(net_amount)})

            total_amount = net_amount + total_amount
        
        #     #validation for total_amount
        if  total_amount != data['total_amount']:
                raise serializers.ValidationError(
                  'total_amount calculation {} not valid: should be {}'.format(data['total_amount'], total_amount)
            )
        return data 



# class SavePurchaseOrderReceivedPovMainSerializer(serializers.ModelSerializer):
    
#     purchase_details = SavePurchaseDetailSerializer(many=True)
#     supplier_name = serializers.ReadOnlyField(source='supplier.name', allow_null=True)
    
#     class Meta:
#         model = PurchaseMain
#         fields = "__all__"
#         read_only_fields = ['created_by', 'created_date_ad', 'created_date_bs','device_type','app_type']



#     def create(self, validated_data):
      
#         self.create_validate(validated_data)
#         # validated_data['created_by'] = current_user.get_created_by(self.context)
#         date_now = timezone.now()

#         purchase_details = validated_data.pop('purchase_details')
        
#         purchase_order_received_main = PurchaseOrderReceivedMain.objects.create(purchase_order_received_type = 2, total_amount  = validated_data['total_amount'], created_by = current_user.get_created_by(self.context), created_date_ad=date_now)
      
#         for purchase_detail in purchase_details:
           
#             PurchaseOrderReceivedDetail.objects.create(**purchase_detail, purchase_order_received_main=purchase_order_received_main,
#                                           created_by=validated_data['created_by'], created_date_ad=date_now)
             
#         return purchase_order_received_main



class SavePurchaseOrderReceivedMainSerializer(serializers.ModelSerializer):
    '''
    model serializer for save purchase order received  main
    '''
    purchase_order_received_details = SavePurchaseOrderReceivedDetailSerializer(many=True)
    supplier_name = serializers.ReadOnlyField(source='supplier.name', allow_null=True)
    
    class Meta:
        model = PurchaseOrderReceivedMain
        fields = "__all__"
        read_only_fields = ['created_by', 'created_date_ad', 'created_date_bs','device_type','app_type']


    def to_representation(self, instance):
        data =  super().to_representation(instance)
        if data['supplier']  is not None:
            supplier = Supplier.objects.get(id=data["supplier"])
            supplier_data = GetSupplierSerializer(supplier)
            data['supplier'] = supplier_data.data
        return data



    def create(self, validated_data):
        '''
        create method for save purchase order received main
        '''
        # print(validated_data, " thi is pov data")
        self.create_validate(validated_data)
        validated_data['created_by'] = current_user.get_created_by(self.context)
        date_now = timezone.now()
        purchase_order_received_details = validated_data.pop('purchase_order_received_details')
        
        purchase_order_received_main = PurchaseOrderReceivedMain.objects.create(**validated_data, created_date_ad=date_now)

    
        for purchase_order_received_detail in purchase_order_received_details:
           
           PurchaseOrderReceivedDetail.objects.create(**purchase_order_received_detail, purchase_order_received_main=purchase_order_received_main,
                                          created_by=validated_data['created_by'], created_date_ad=date_now)
                                          
        return purchase_order_received_main   




    def create_validate(self, data):
        '''
        validation method for create purchase order received main
        '''
        decimal.getcontext().rounding=decimal.ROUND_HALF_UP
        quantize_places = Decimal(10) ** -2
        total_amount = Decimal('0.00')
        net_amount = Decimal('0.00')
        purchase_order_received_details = data['purchase_order_received_details']
      

        for purchase_order_received in purchase_order_received_details:
            purchase_order_received_detail = {}
            key_values = zip(purchase_order_received.keys(), purchase_order_received.values())
            for key, values in key_values:
                purchase_order_received_detail[key] = values
              
            
            if  purchase_order_received_detail['amount'] <= 0 or    purchase_order_received_detail['qty'] <=0:
                raise serializers.ValidationError({
                    f'item {  purchase_order_received_detail ["item"].brand_name}': 'values in fields, amount and  quantity  cannot be less than'
                                                            ' or equals to 0'})

            if  purchase_order_received_detail['discount_rate'] < 0 or   purchase_order_received_detail['net_amount'] < 0 or    purchase_order_received_detail['sub_total'] < 0:
                    raise serializers.ValidationError({
                        f'item {  purchase_order_received_detail["item"].brand_name}': 'values in field, discount rate, net_amount, sub_total cannot be less than 0'})

            #validation for discount amount

            discount_rate = (  purchase_order_received_detail['discount_amount'] *
                                 Decimal('100')) / (purchase_order_received_detail['amount'] *
                                                     purchase_order_received_detail['qty'])
            discount_rate = discount_rate.quantize(quantize_places)

            discount_amount = (purchase_order_received_detail['discount_amount']).quantize(quantize_places)
            #validation for sub_total
            sub_total =   purchase_order_received_detail['amount']* purchase_order_received_detail['qty']
            sub_total = sub_total.quantize(quantize_places)

            net_amount = Decimal(sub_total-discount_amount)
            net_amount = net_amount.quantize(quantize_places)

            if  sub_total!=   purchase_order_received_detail['sub_total']:
                raise serializers.ValidationError({f'item {  purchase_order_received_detail["item"].brand_name}':
                    f'sub_total calculation not valid : should be {sub_total }'})

            if net_amount !=   purchase_order_received_detail['net_amount']:
                raise serializers.ValidationError({f'item {  purchase_order_received_detail["item"].brand_name}':
                    'net_amount calculation not valid : should be {}'.format(net_amount)})

            total_amount = net_amount + total_amount
            # print( data['total_amount'])
            # print(total_amount)

        if  total_amount != data['total_amount']:
                raise serializers.ValidationError(
                  'total_amount calculation {} not valid: should be {}'.format(data['total_amount'], total_amount)
            )
        return data 


class UpdatePurchaseOrderMainSerializer(serializers.ModelSerializer):
    assigned_to_user_name = serializers.ReadOnlyField(source='assigned_to.user_name', allow_null=True, default = "")
    assigned_to_first_name = serializers.ReadOnlyField(source='assigned_to.first_name', allow_null=True ,default = "")
    assigned_to_last_name = serializers.ReadOnlyField(source='assigned_to.last_name', allow_null=True ,default = "")
    
    class Meta:
        model = PurchaseOrderMain
        fields = ['assigned_to', 'assigned_to_first_name','assigned_to_user_name','assigned_to_last_name']
        read_only_fields =  [ 'assigned_to_first_name','assigned_to_user_name',' assigned_to_last_name']

   
    def update(self, instance, validated_data): 
        instance.assigned_to = validated_data.get('assigned_to', instance.assigned_to)
        instance.save()
        return instance



class DeletePurchaseOrderReceivedDetailSerializer(serializers.ModelSerializer):
    item_price=  serializers.ReadOnlyField(source="item.price", allow_null=True)
    item_name = serializers.ReadOnlyField(source="item.brand_name", allow_null=True)
    item_unit_name = serializers.ReadOnlyField(source="item_unit.name", allow_null=True)

    class Meta:
        model =PurchaseOrderReceivedDetail
        fields =  "__all__"   



   