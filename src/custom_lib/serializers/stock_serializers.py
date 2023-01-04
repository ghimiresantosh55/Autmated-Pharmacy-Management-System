from rest_framework import serializers
from src.sale.models import SaleDetail, SaleMain
from src.purchase.models import PurchaseDetail
from src.custom_lib.functions import stock
from src.item.models import Item


class PurchaseDetailStockSerializer(serializers.ModelSerializer):
    '''
    purchase detail serializer for write_only views
    '''
    item_name = serializers.ReadOnlyField(source='item.brand_name')
    discount_rate =  serializers.ReadOnlyField(source='item.discount_rate', allow_null=True)
    company_discount_rate = serializers.ReadOnlyField(source='item.company.discount_rate', allow_null=True)
    item_unit_name =  serializers.ReadOnlyField(source='item.item_unit.name', allow_null=True)
    unit_short_form = serializers.ReadOnlyField(source='item.item_unit.short_form', allow_null=True)
    remaining_qty = serializers.SerializerMethodField()
    return_qty = serializers.SerializerMethodField()
    sale_qty = serializers.SerializerMethodField()
    sale_return_qty = serializers.SerializerMethodField()

    # def get_qty(self, product):
    #     PurchaseDetail.objects.filter(rem_qty__gt=0.00)
    #     ref_purchase_detail = purchase_detail.id
    #     serializer = stock.get_remaining_qty_of_purchase(ref_purchase_detail)
    #     return serializer.data
    class Meta:
        model = PurchaseDetail
        exclude = ['discount_amount','net_amount', 'created_date_ad',
                   'created_date_bs', 'created_by']
      

    def get_remaining_qty(self, purchase_detail):
        '''
        method for get remaining quantity
        '''
        ref_purchase_detail = purchase_detail.id
        purchase_rem_qty = stock.get_remaining_qty_of_purchase(ref_purchase_detail)

        return purchase_rem_qty

    def get_return_qty(self, purchase_detail):
        '''
        method for get return quantity
        '''
        ref_purchase_detail = purchase_detail.id
        return_rem_qty = stock.get_purchase_return_qty(ref_purchase_detail)
        return return_rem_qty


    def get_sale_qty(self, purchase_detail):
        '''
        method for get sale quantity
        '''
        ref_purchase_detail = purchase_detail.id
        sale_rem_qty = stock.get_purchase_sale_qty(ref_purchase_detail)
        return sale_rem_qty

    def get_sale_return_qty(self, purchase_detail):
        '''
        method for get  sale return quantity
        '''
        ref_purchase_detail = purchase_detail.id
        rem_qty = stock.get_purchase_sale_return_qty(ref_purchase_detail)
        return rem_qty


class StockAnalysisSerializer(serializers.ModelSerializer):
    '''
    model serializer for stock analysis
    '''
    remaining_qty = serializers.SerializerMethodField()
    return_qty = serializers.SerializerMethodField()
    sale_qty = serializers.SerializerMethodField()
    sale_return_qty = serializers.SerializerMethodField()
    purchase_qty = serializers.SerializerMethodField()
    company_discount_rate = serializers.ReadOnlyField(source='company.discount_rate', allow_null=True)
    item_unit_name =  serializers.ReadOnlyField(source='item_unit.name', allow_null=True)
    unit_short_form = serializers.ReadOnlyField(source='item_unit.short_form', allow_null=True)

    class Meta:
        model = Item
        exclude= ['device_type','app_type','item_details','image', 'product_category', 'generic_name',  'created_date_ad', 'created_date_bs', 
        'created_by','archived', 'verified','medicine_form','company','active']

    def get_remaining_qty(self, item):
        item_id = item.id
        rem_qty = stock.get_remaining_qty_of_item(item_id)
        # if rem_qty>0:
        return rem_qty

    def get_return_qty(self, item):
        item_id = item.id
        rem_qty = stock.get_purchase_return_qty_of_item(item_id)
        return rem_qty


    def get_sale_qty(self, item):
        item_id = item.id
        rem_qty = stock.get_sale_qty_of_item(item_id)
        return rem_qty

    def get_sale_return_qty(self, item):
        item_id = item.id
        rem_qty = stock.get_sale_return_qty_of_item(item_id)
        return rem_qty

    def get_purchase_qty(self, item):
        item_id = item.id
        rem_qty = stock.get_purchase_qty_of_item(item_id)
        return rem_qty



class StockAnalysisForBillingSerializer(serializers.ModelSerializer):
    '''
    model serializer for stock analysis
    '''
    remaining_qty = serializers.SerializerMethodField()
    return_qty = serializers.SerializerMethodField()
    sale_qty = serializers.SerializerMethodField()
    sale_return_qty = serializers.SerializerMethodField()
    purchase_qty = serializers.SerializerMethodField()
    company_discount_rate = serializers.ReadOnlyField(source='company.discount_rate', allow_null=True)
    item_unit_name =  serializers.ReadOnlyField(source='item_unit.name', allow_null=True)
    unit_short_form = serializers.ReadOnlyField(source='item_unit.short_form', allow_null=True)

    class Meta:
        model = Item
        exclude= ['device_type','app_type','item_details','image', 'product_category', 'generic_name',  'created_date_ad', 'created_date_bs', 
        'created_by','archived', 'verified','medicine_form','company','active']

    def get_remaining_qty(self, item):
        item_id = item.id
        rem_qty = stock.get_remaining_qty_of_item(item_id)
        # if rem_qty>0:
        return rem_qty

    def get_return_qty(self, item):
        item_id = item.id
        rem_qty = stock.get_purchase_return_qty_of_item(item_id)
        return rem_qty


    def get_sale_qty(self, item):
        item_id = item.id
        rem_qty = stock.get_sale_qty_of_item(item_id)
        return rem_qty

    def get_sale_return_qty(self, item):
        item_id = item.id
        rem_qty = stock.get_sale_return_qty_of_item(item_id)
        return rem_qty

    def get_purchase_qty(self, item):
        item_id = item.id
        rem_qty = stock.get_purchase_qty_of_item(item_id)
        return rem_qty



class OrderAnalysisSerializer(serializers.ModelSerializer):
    '''
    model serializer for stock analysis
    '''
    
    # item_name = serializers.ReadOnlyField(source='item.name')
    # chalan_no = serializers.ReadOnlyField(source='purchase.chalan_no')
  
    remaining_qty = serializers.SerializerMethodField()
    return_qty = serializers.SerializerMethodField()
    sale_qty = serializers.SerializerMethodField()
    sale_return_qty = serializers.SerializerMethodField()
    purchase_qty = serializers.SerializerMethodField()
    purchase_order_qty = serializers.SerializerMethodField()
    purchase_received_qty = serializers.SerializerMethodField()
    customer_order_qty = serializers.SerializerMethodField()

    class Meta:
        model = Item
        exclude= ['device_type','app_type','item_details','image', 'product_category', 'generic_name',  'created_date_ad', 'created_date_bs', 'archived', 'verified','medicine_form','company','active']

    def get_remaining_qty(self, item):
        item_id = item.id
        rem_qty = stock.get_remaining_qty_of_item(item_id)
        return rem_qty

    def get_return_qty(self, item):
        item_id = item.id
        rem_qty = stock.get_purchase_return_qty_of_item(item_id)
        return rem_qty


    def get_sale_qty(self, item):
        item_id = item.id
        rem_qty = stock.get_sale_qty_of_item(item_id)
        return rem_qty

    def get_sale_return_qty(self, item):
        item_id = item.id
        rem_qty = stock.get_sale_return_qty_of_item(item_id)
        return rem_qty

    def get_purchase_qty(self, item):
        item_id = item.id
        rem_qty = stock.get_item_purchase_qty(item_id)
        return rem_qty

    def get_purchase_order_qty(self, item):
        item_id = item.id
        rem_qty = stock.get_item_purchase_order_qty(item_id)
        return rem_qty


    def get_purchase_received_qty(self, item):
        item_id = item.id
        rem_qty = stock.get_item_purchase_received_qty(item_id)
        return rem_qty
    
    def get_customer_order_qty(self, item):
        item_id = item.id
        rem_qty = stock.get_item_pending_customer_order_qty(item_id)
        return rem_qty



class ItemStockListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['brand_name', 'id']



# class ItemLedgerSaleSerializer(serializers.ModelSerializer):

#     supplier_customer_name=  serializers.ReadOnlyField(source = 'sale_main.customer.first_name', allow_null=True)
#     supplier_customer= serializers.ReadOnlyField(source = 'sale_main.customer.id', allow_null=True)
#     op_type =  serializers.ReadOnlyField(source='sale_main.get_sale_type_display', allow_null=True)
   
#     class Meta:
#         model = SaleDetail
#         fields = ['created_date_ad','created_date_bs','qty','item','amount','supplier_customer_name','supplier_customer','op_type']
#         # extra_kwargs = {'supplier_customer_name': {'required': True},'supplier_customer':{'required': True},'op_type':{'required': True}}



# class ItemLedgerPurchaseSerializer(serializers.ModelSerializer):
#     supplier_customer_name=  serializers.ReadOnlyField(source = 'purchase_main.supplier.name', allow_null=True)
#     supplier_customer= serializers.ReadOnlyField(source = 'purchase_main.supplier.id', allow_null=True)
#     op_type =  serializers.ReadOnlyField(source='purchase_main.get_purchase_type_display', allow_null=True)
    
#     class Meta: 
#         model = PurchaseDetail
#         fields = ['created_date_ad','created_date_bs','qty','item','amount','supplier_customer_name','supplier_customer','op_type']





