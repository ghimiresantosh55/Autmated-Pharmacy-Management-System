from rest_framework import serializers
from src.supplier.models import Supplier
from .models import PurchaseMain, PurchaseDetail
from src.purchase_order.models import PurchaseOrderReceivedMain, PurchaseOrderReceivedDetail
from decimal import Decimal
from django.utils import timezone
from src.custom_lib.functions import current_user
import decimal
from decimal import Decimal
from rest_framework import serializers
from src.supplier.models import Supplier
from django.utils import timezone
from src.custom_lib.functions import current_user
from src.purchase_order.purchase_order_unique_id_generator import  generate_purchase_order_received_no


class GetSupplierSerializer(serializers.ModelSerializer): 
    '''
    model serializer for get supplier data listing
    '''
    class Meta:
        model = Supplier
        exclude = ['created_date_ad','created_date_bs','active','created_by','device_type','app_type',]


class GetSupplierForDirectPurchaseSerializer(serializers.ModelSerializer): 
    '''
    model serializer for get supplier data listing
    '''
    class Meta:
        model = Supplier
        exclude = ['created_date_ad','created_date_bs','active','created_by','device_type','app_type','address','phone_no','pan_vat_no','latitude','longitude']


class GetSupplierForReturnPurchaseSerializer(serializers.ModelSerializer): 
    
    class Meta:
        model = Supplier
        exclude = ['created_date_ad','created_date_bs','active','created_by','device_type','app_type','address','phone_no','pan_vat_no','latitude','longitude']


class GetRefPurchaseReturnSerializer(serializers.ModelSerializer): 
    
    class Meta:
        model = PurchaseMain
        exclude = ['created_date_ad','created_date_bs','created_by','device_type','app_type','purchase_type','pay_type','supplier','total_amount','discount_amount',\
          'vat_amount','bill_no' ,'bill_date_ad','bill_date_bs','ref_purchase' ,'ref_purchase_order_received_main','remarks']


class ListPurchaseDetailSerializer(serializers.ModelSerializer):
    '''
    model serializer for get listing of purchase detail table data
    '''
    item_name = serializers.ReadOnlyField(source='item.brand_name', allow_null=True)
    item_price =  serializers.ReadOnlyField(source='item.price', allow_null=True)

    class Meta:
        model = PurchaseDetail
        exclude = ['purchase_main']

    # def to_representation(self, instance):
    #     '''
    #     method for get item object
    #     '''
    #     data =  super().to_representation(instance)
    #     item = Item.objects.get(id=data["item"])
    #     item_data = GetItemSerializer(item)
    #     data['item'] = item_data.data
    #     return data
    

class ListPurchaseMainSerializer(serializers.ModelSerializer): 
    '''
    model serializer for get listing of purchase main table data
    '''
    purchase_details = ListPurchaseDetailSerializer(many=True)
    purchase_type_display = serializers.ReadOnlyField(source='get_purchase_type_display', allow_null=True)
    supplier_name = serializers.ReadOnlyField(source='supplier.name', allow_null=True)
    class Meta:
        model = PurchaseMain
        fields = '__all__'

    def to_representation(self, instance):
        '''
        method for get supplier object
        '''
        data =  super().to_representation(instance)
        if data['supplier']  is not None:
            supplier = Supplier.objects.get(id=data["supplier"])
            supplier_data = GetSupplierSerializer(supplier)
            data['supplier'] =  supplier_data.data
        return data



class SavePurchaseDetailSerializer(serializers.ModelSerializer):
    '''
    model serializer for  save purchase detail data
    '''
    item_name = serializers.ReadOnlyField(source='item.brand_name', allow_null=True)
    created_by_user_name = serializers.ReadOnlyField(source='created_by.user_name', allow_null=True)
    class Meta:
        model = PurchaseDetail
        exclude = ['purchase_main']
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



class SavePurchaseMainSerializer(serializers.ModelSerializer):
    '''
    model serializer for save purchase data
    '''
    purchase_details = SavePurchaseDetailSerializer(many=True)
    purchase_type_display = serializers.ReadOnlyField(source='get_purchase_type_display', allow_null=True)
    supplier_name = serializers.ReadOnlyField(source='supplier.name', allow_null=True)
    class Meta:
        model = PurchaseMain
        fields = "__all__"
        read_only_fields = ['created_by', 'created_date_ad', 'created_date_bs','device_type','app_type']


    def to_representation(self, instance):
        my_fields = { 'ref_purchase', 'ref_purchase_order'}
                   
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
        create method for save purchase
        '''
        self.create_validate(validated_data)
    
        validated_data['created_by'] = current_user.get_created_by(self.context)
        date_now = timezone.now()
        purchase_details = validated_data.pop('purchase_details')
        purchase_main = PurchaseMain.objects.create(**validated_data, created_date_ad=date_now)
        
        for purchase_detail in purchase_details:
       
           PurchaseDetail.objects.create(**purchase_detail, purchase_main=purchase_main,
                                          created_by=validated_data['created_by'], created_date_ad=date_now)

        return  purchase_main



    def create_validate(self, data):
        '''
        validation for create method of save opening stock
        '''
        decimal.getcontext().rounding=decimal.ROUND_HALF_UP
        quantize_places = Decimal(10) ** -2
        total_amount = Decimal('0.00')
        net_amount = Decimal('0.00')
        purchase_details = data['purchase_details']


        for purchase in purchase_details:
            purchase_detail = {}
            key_values = zip(purchase.keys(), purchase.values())
            for key, values in key_values:
                purchase_detail[key] = values
          

            if  purchase_detail['amount'] <= 0 or  purchase_detail['qty'] <=0 :
                raise serializers.ValidationError({
                    f'item {purchase_detail["item"].brand_name}': 'values in fields, amount and  quantity  cannot be less than'
            
                                                            ' or equals to 0'})

            if  purchase_detail['discount_rate'] < 0 or  purchase_detail['net_amount'] < 0 or  purchase_detail['sub_total'] < 0:
                    raise serializers.ValidationError({
                        f'item {purchase_detail["item"].brand_name}': 'values in field, discount rate, net_amount, sub_total cannot be less than 0'})

            # validation for discount amount
            # discount_rate = (purchase_detail['discount_amount'] *
            #                      Decimal('100')) / (purchase_detail['amount'] *
            #                                         purchase_detail['qty'])
            discount_rate = (0.00)

            
            #validation for sub_total
            sub_total = purchase_detail['amount'] * purchase_detail['qty']
            sub_total = sub_total.quantize(quantize_places)

            # net_amount = (sub_total-(purchase_detail['amount']*purchase_detail['qty']*purchase_detail['discount_rate'])/Decimal('100'))
            net_amount= (sub_total)
            net_amount = net_amount.quantize(quantize_places)
            # print(net_amount, "this is net amount")
            if net_amount != purchase_detail['net_amount']:
                raise serializers.ValidationError({f'item {purchase_detail["item"].brand_name}':
                    'net_amount calculation not valid : should be {}'.format(net_amount)})

            if  sub_total!= purchase_detail['sub_total']:
                raise serializers.ValidationError({f'item {purchase_detail["item"].brand_name}':
                    f'sub_total calculation not valid : should be {sub_total }'})
           
            total_amount = net_amount +total_amount
        total_amount = total_amount - data['discount_amount']
        # total_amount= total_amount-purchase_detail['discount_amount']
        if  total_amount != data['total_amount']:
                raise serializers.ValidationError(
                  'total_amount calculation {} not valid: should be {}'.format(data['total_amount'], total_amount)
            )
        return data 


class SavePurchaseOpeningStockDetailSerializer(serializers.ModelSerializer):
    '''
    model serializer for save purchase opening stock detail
    '''
    item_name = serializers.ReadOnlyField(source='item.brand_name', allow_null=True)
    item_price= serializers.ReadOnlyField(source='item.price', allow_null=True)
    created_by_user_name = serializers.ReadOnlyField(source='created_by.user_name', allow_null=True)

    class Meta:
        model = PurchaseDetail
        exclude = ['purchase_main']
        read_only_fields = ['created_by', 'created_date_ad', 'created_date_bs','device_type','app_type']


    


class SaveOpeningStockSerializer(serializers.ModelSerializer):
    '''
    model serializer for save purchase opening stock 
    '''
    purchase_details = SavePurchaseOpeningStockDetailSerializer(many=True)
    created_by_user_name = serializers.ReadOnlyField(source='created_by.user_name', allow_null=True)
    purchase_type_display = serializers.ReadOnlyField(source='get_purchase_type_display', allow_null=True)
    # supplier_name = serializers.ReadOnlyField(source='supplier.name', allow_null=True)
    class Meta:
        model = PurchaseMain
        fields = "__all__"   
        read_only_fields = ['device_type','app_type','created_by', 'created_date_ad', 'created_date_bs']


    def create(self, validated_data):
        '''
        create method for save opening stock
        '''
        self.create_validate(validated_data)
        validated_data['created_by'] = current_user.get_created_by(self.context)
        date_now = timezone.now()
        purchase_details = validated_data.pop('purchase_details')


        purchase_main = PurchaseMain.objects.create(**validated_data, created_date_ad=date_now)

        for purchase_detail in purchase_details:
            PurchaseDetail.objects.create(**purchase_detail, purchase_main=purchase_main,
                                          created_by=validated_data['created_by'], created_date_ad=date_now)
        
        return purchase_main
    
        
    
    def create_validate(self, data):
        '''
        validation for create method of save opening stock
        '''
        decimal.getcontext().rounding=decimal.ROUND_HALF_UP
        quantize_places = Decimal(10) ** -2
        total_amount = Decimal('0.00')
        net_amount = Decimal('0.00')
        purchase_details = data['purchase_details']
      

        for purchase in purchase_details:
            purchase_detail = {}
            key_values = zip(purchase.keys(), purchase.values())
            for key, values in key_values:
                purchase_detail[key] = values
            
            if  purchase_detail['amount'] <= 0 or  purchase_detail['qty'] <=0 :
                raise serializers.ValidationError({
                    f'item {purchase_detail["item"].brand_name}': 'values in fields, amount and  quantity  cannot be less than'
            
                                                            ' or equals to 0'})

            if  purchase_detail['discount_rate'] < 0 or  purchase_detail['net_amount'] < 0 or  purchase_detail['sub_total'] < 0:
                    raise serializers.ValidationError({
                        f'item {purchase_detail["item"].brand_name}': 'values in field, discount rate, net_amount, sub_total cannot be less than 0'})

            # validation for discount amount
            # discount_rate = (purchase_detail['discount_amount'] *
            #                      Decimal('100')) / (purchase_detail['amount'] *
            #                                         purchase_detail['qty'])
            # discount_rate = discount_rate.quantize(quantize_places)

            #validation for sub_total
            discount_rate = (0.00)
            sub_total = purchase_detail['amount'] * purchase_detail['qty']
            sub_total = sub_total.quantize(quantize_places)

            
            # net_amount =  ((purchase_detail['amount'] * purchase_detail['qty'])-((purchase_detail['amount']*['qty']*purchase_detail['discount_rate'])/Decimal('100')))
            net_amount= (sub_total)
            net_amount = net_amount.quantize(quantize_places)

            if net_amount != purchase_detail['net_amount']:
                raise serializers.ValidationError({f'item {purchase_detail["item"].brand_name}':
                    'net_amount calculation not valid : should be {}'.format(net_amount)})

            if  sub_total!= purchase_detail['sub_total']:
                raise serializers.ValidationError({f'item {purchase_detail["item"].brand_name}':
                    f'sub_total calculation not valid : should be {sub_total }'})

            total_amount = net_amount + total_amount
            #validation for total_amount
        total_amount = total_amount - data['discount_amount']
        if  total_amount != data['total_amount']:
              
                raise serializers.ValidationError(
                  'total_amount calculation {} not valid: should be {}'.format(data['total_amount'], total_amount)
            )
        return data 



class SavePurchaseMainForReturnSerializer(serializers.ModelSerializer):
    '''
    model serializer for save purchase main for return data
    '''
    purchase_details = SavePurchaseDetailSerializer(many=True)
    purchase_type_display = serializers.ReadOnlyField(source='get_purchase_type_display', allow_null=True)
    # supplier_name = serializers.ReadOnlyField(source='supplier.name', allow_null=True)
    class Meta:
        model = PurchaseMain
        fields = "__all__"
        read_only_fields = ['created_by', 'created_date_ad', 'created_date_bs','device_type','app_type']


    # def to_representation(self, instance):
    #     my_fields = { 'ref_purchase', 'ref_purchase_order'}
                   
    #     data = super().to_representation(instance)
    #     for field in my_fields:
    #         try:
    #             if not data[field]:
    #                 data[field] = ""
    #         except KeyError:
    #             pass
    #     return data

    def to_representation(self, instance):
        my_fields = { 'ref_purchase', 'ref_purchase_order'}
        data =  super().to_representation(instance)
       
        if data['supplier']  is not None:
            supplier = Supplier.objects.get(id=data["supplier"])
            supplier_data = GetSupplierForReturnPurchaseSerializer(supplier)
            data['supplier'] =  supplier_data.data

        if data['ref_purchase'] is not None:
            ref_purchase= PurchaseMain.objects.get(id=data["ref_purchase"])
            ref_purchase_data= GetRefPurchaseReturnSerializer(ref_purchase)
            data['ref_purchase'] = ref_purchase_data.data

            for field in my_fields:
                try:
                    if not data[field]:
                        data[field] = ""
                except KeyError:
                    pass

        return data


    def create(self, validated_data):
        '''
        create method for save purchase
        '''
        self.create_validate(validated_data)
        validated_data['created_by'] = current_user.get_created_by(self.context)
        date_now = timezone.now()
        purchase_details = validated_data.pop('purchase_details')

        purchase_main = PurchaseMain.objects.create(**validated_data, created_date_ad=date_now)
         

        for purchase_detail in purchase_details:
            PurchaseDetail.objects.create(**purchase_detail, purchase_main=purchase_main,
                                          created_by=validated_data['created_by'], created_date_ad=date_now)

        return purchase_main


    def create_validate(self, data):
        '''
        validation for create save purchase
        '''
        decimal.getcontext().rounding=decimal.ROUND_HALF_UP
        quantize_places = Decimal(10) ** -2
        total_amount = Decimal('0.00')
        net_amount = Decimal('0.00')
        purchase_details = data['purchase_details']
      

        for purchase in purchase_details:
            purchase_detail = {}
            key_values = zip(purchase.keys(), purchase.values())
            for key, values in key_values:
                purchase_detail[key] = values
            
            if  purchase_detail['amount'] <= 0 or  purchase_detail['qty'] <=0 :
                raise serializers.ValidationError({
                    f'item {purchase_detail["item"].brand_name}': 'values in fields, amount and  quantity  cannot be less than'
            
                                                            ' or equals to 0'})

            if  purchase_detail['discount_rate'] < 0 or  purchase_detail['net_amount'] < 0 or  purchase_detail['sub_total'] < 0:
                    raise serializers.ValidationError({
                        f'item {purchase_detail["item"].brand_name}': 'values in field, discount rate, net_amount, sub_total cannot be less than 0'})

            # validation for discount amount
            # discount_rate = (purchase_detail['discount_amount'] *
            #                      Decimal('100')) / (purchase_detail['amount'] *
            #                                         purchase_detail['qty'])
            # discount_rate = discount_rate.quantize(quantize_places)
            discount_rate = (0.00)

            #validation for sub_total
            sub_total = purchase_detail['amount'] * purchase_detail['qty']
            sub_total = sub_total.quantize(quantize_places)

            # net_amount =  ((purchase_detail['amount'] * purchase_detail['qty'])-(
            #         (purchase_detail['amount']*purchase_detail['qty']*purchase_detail['discount_rate'])/Decimal('100')
            # ))
            net_amount= (sub_total)
            net_amount = net_amount.quantize(quantize_places)

            if net_amount != purchase_detail['net_amount']:
                raise serializers.ValidationError({f'item {purchase_detail["item"].brand_name}':
                    'net_amount calculation not valid : should be {}'.format(net_amount)})

            if  sub_total!= purchase_detail['sub_total']:
                raise serializers.ValidationError({f'item {purchase_detail["item"].brand_name}':
                    f'sub_total calculation not valid : should be {sub_total }'})

            total_amount = net_amount + total_amount
            #validation for total_amount
        total_amount = total_amount - data['discount_amount']
        if  total_amount != data['total_amount']:
              
                raise serializers.ValidationError(
                  'total_amount calculation {} not valid: should be {}'.format(data['total_amount'], total_amount)
            )
        return data 


class UpdatePurchaseDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PurchaseDetail
        exclude=['purchase_main']
        read_only_fields = ['created_date_ad','created_date_bs','created_by','device_type','app_type']
      
    def update(self, instance, validated_data): 
        instance.item = validated_data.get('item', instance.item)
        instance.qty = validated_data.get('qty', instance.qty)
        instance.item_unit = validated_data.get('item_unit', instance.item_unit)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.discount_rate = validated_data.get('discount_rate', instance.discount_rate)
        instance.discount_amount = validated_data.get('discount_amount', instance.discount_amount)
        instance.net_amount = validated_data.get('net_amount', instance.net_amount)
        instance.sub_total = validated_data.get('sub_total', instance.sub_total)
        instance.location = validated_data.get('location', instance.location)
        instance.save()
        return instance



class DirectpurchaseSerializer(serializers.ModelSerializer):
   
    purchase_details = SavePurchaseDetailSerializer(many=True)
    purchase_type_display = serializers.ReadOnlyField(source='get_purchase_type_display', allow_null=True)
    # supplier_name = serializers.ReadOnlyField(source='supplier.name', allow_null=True)
    class Meta:
        model = PurchaseMain
        fields = "__all__"
        read_only_fields = ['created_by', 'created_date_ad', 'created_date_bs','device_type','app_type']
    

    
    def to_representation(self, instance):
        '''
        method for get supplier object
        '''
        my_fields = { 'ref_purchase', 'ref_purchase_order'}
        data =  super().to_representation(instance)
        for field in my_fields:
            try:
                if not data[field]:
                    data[field] = ""
            except KeyError:
                pass
        if data['supplier']  is not None:
            supplier = Supplier.objects.get(id=data["supplier"])
            supplier_data = GetSupplierForDirectPurchaseSerializer(supplier)
            data['supplier'] =  supplier_data.data
        return data



    def create(self, validated_data):
        self.create_validate(validated_data)
        validated_data['created_by'] = current_user.get_created_by(self.context)
        date_now = timezone.now()
        purchase_details = validated_data.pop('purchase_details')

        purchase_main = PurchaseMain.objects.create(**validated_data, created_date_ad=date_now)
         

        for purchase_detail in purchase_details:
            PurchaseDetail.objects.create(**purchase_detail, purchase_main=purchase_main,
                                          created_by=validated_data['created_by'], created_date_ad=date_now)

        return purchase_main


    def create_validate(self, data):
        decimal.getcontext().rounding=decimal.ROUND_HALF_UP
        quantize_places = Decimal(10) ** -2
        total_amount = Decimal('0.00')
        net_amount = Decimal('0.00')
        purchase_details = data['purchase_details']
      

        for purchase in purchase_details:
            purchase_detail = {}
            key_values = zip(purchase.keys(), purchase.values())
            for key, values in key_values:
                purchase_detail[key] = values
            
            if  purchase_detail['amount'] <= 0 or  purchase_detail['qty'] <=0 :
                raise serializers.ValidationError({
                    f'item {purchase_detail["item"].brand_name}': 'values in fields, amount and  quantity  cannot be less than'
            
                                                            ' or equals to 0'})

            if  purchase_detail['discount_rate'] < 0 or  purchase_detail['net_amount'] < 0 or  purchase_detail['sub_total'] < 0:
                    raise serializers.ValidationError({
                        f'item {purchase_detail["item"].brand_name}': 'values in field, discount rate, net_amount, sub_total cannot be less than 0'})

            # validation for discount amount
            # discount_rate = (purchase_detail['discount_amount'] *
            #                      Decimal('100')) / (purchase_detail['amount'] *
            #                                         purchase_detail['qty'])
            # discount_rate = discount_rate.quantize(quantize_places)
            discount_rate = (0.00)

            #validation for sub_total
           
            sub_total = purchase_detail['amount'] * purchase_detail['qty']
            
            sub_total = sub_total.quantize(quantize_places)
            # print(((purchase_detail['amount']*purchase_detail['qty']*purchase_detail['discount_rate'])/Decimal('100')),"this is discount amount")

            # net_amount = (purchase_detail['amount'] * purchase_detail['qty'])-(purchase_detail['amount']*purchase_detail['qty']*purchase_detail['discount_rate']/Decimal('100'))
            net_amount= (sub_total)
            net_amount = net_amount.quantize(quantize_places)
            # print(net_amount, " this is after quantize")

            if net_amount != purchase_detail['net_amount']:
                raise serializers.ValidationError({f'item {purchase_detail["item"].brand_name}':
                    'net_amount calculation not valid : should be {}'.format(net_amount)})


            if  sub_total!= purchase_detail['sub_total']:
                raise serializers.ValidationError({f'item {purchase_detail["item"].brand_name}':
                    f'sub_total calculation not valid : should be {sub_total }'})

            total_amount = net_amount + total_amount
            #validation for total_amount
        total_amount = total_amount - data['discount_amount']
        if  total_amount != data['total_amount']:
              
                raise serializers.ValidationError(
                  'total_amount calculation {} not valid: should be {}'.format(data['total_amount'], total_amount)
            )
        return data 
   
   