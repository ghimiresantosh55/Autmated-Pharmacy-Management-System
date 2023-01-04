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
from src.custom_lib.functions.stock import get_item_pending_customer_order_qty_for_create_po, get_remaining_qty_of_item, get_purchase_order_unverified_qty, get_pending_customer_order_qty

quantize_places = Decimal(10) ** -2
def create_purchase_order(customer_order_data, request, supplier_priority: int):
    """
    function to create purchase order from customer order data
    """
    purchase_order_data_list = []
    purchase_order_detail_data_list = []
    customer_order_details = customer_order_data['order_details']
    # print(customer_order_details, "customer order details")
    
    #print(customer_order_details, " this is customer order detail data")
    for customer_order_detail in customer_order_details:
        
        try:
            company_id = Item.objects.get(id=customer_order_detail['item']).company.id
            supplier_id = PoPriority.objects.filter(company=company_id, priority=supplier_priority).values_list("supplier", flat=True)[0]
            # print(supplier_id, "this is priority supplier ids")
            # print(supplier_priority, " this is supplier priority")
        except Exception as e:
            supplier_id = None

        # Validation if unit is blank in customer order
        if customer_order_detail['item_unit'] is None or customer_order_detail['item_unit']=="":
            item_unit = None
        else:
            item_unit = customer_order_detail['item_unit']['id']
        
        stock_of_item = get_remaining_qty_of_item(customer_order_detail['item']) + get_purchase_order_unverified_qty(customer_order_detail['item'])
        # stock_of_item -= get_pending_customer_order_qty(customer_order_detail['item'], customer_order_detail['id'])
        stock_of_item -= get_item_pending_customer_order_qty_for_create_po(customer_order_detail['item'], customer_order_detail['id'])
        # print(stock_of_item, "this is stock of item")
        # 4 > 3 + 6
        if (Decimal(customer_order_detail['qty']) > stock_of_item):
            print("if of co")
            # print(customer_order_detail['item'])
            # check if stock is in negative
            if stock_of_item <= 0:
                purchase_qty = Decimal(customer_order_detail['qty']) 
            else:     
              
                purchase_qty = Decimal(customer_order_detail['qty']) - Decimal(stock_of_item)
                # print(purchase_qty, "this is purchase qty")
            purchase_amount = (Decimal(customer_order_detail['amount'])/Decimal(1.16)).quantize(quantize_places)
           
            sub_total = Decimal(str(purchase_qty *  (Decimal(purchase_amount)))).quantize(quantize_places)
            discount_amount = Decimal(customer_order_detail['discount_amount'])
            net_amount = (Decimal(sub_total - discount_amount))
            purchase_order_detail_data_list.append({
                "available": 1,
                "item": customer_order_detail['item'],
                "qty": purchase_qty,
                "item_unit": item_unit,
                "discount_rate": customer_order_detail['discount_rate'],
                "discount_amount": discount_amount,
                "net_amount": net_amount,
                "amount":  purchase_amount,
                "sub_total": sub_total,
                "supplier": supplier_id
            })
    #filtering item with pending purchase order and adding them directly to PO
    purchase_order_append_data = purchase_order_detail_data_list.copy()
    print("poappend data", purchase_order_append_data)
    # print(purchase_order_append_data,"purchase_order_append_data")
    for purchase_order in purchase_order_append_data:
        try:
            purchase_order_detail_db = PurchaseOrderDetail.objects.filter(available=1).get(item=purchase_order['item'])
            purchase_order_main_db = purchase_order_detail_db.purchase_order_main
            purchase_order_detail_db.qty += Decimal(purchase_order['qty'])
            # sub total calculation and update
            sub_total = Decimal(purchase_order['qty']) * purchase_order_detail_db.amount
            sub_total =sub_total.quantize(quantize_places) # round off
            purchase_order_detail_db.sub_total += sub_total # updated in detail

            # net total calculation and update
            discount_amount = sub_total * Decimal(purchase_order["discount_rate"]) / 100
            discount_amount = discount_amount.quantize(quantize_places) # round off
            purchase_order_detail_db.discount_amount += discount_amount

            net_amount = sub_total - discount_amount
            purchase_order_detail_db.net_amount += net_amount
            # purchase_order_main_db.total_amount += net_amount
            # added statically total amount = 0
            purchase_order_main_db.total_amount = 0

            # print(purchase_order_main_db.total_amount,"this is sum")
            purchase_order_detail_db.save()   
            purchase_order_main_db.save()
            purchase_order_detail_data_list.remove(purchase_order)
        except ObjectDoesNotExist as e:
            pass
    # -------------------------------------------------------------------------
      #  add order to already existing purchase order with same supplier
    purchase_order_detail_data_list_for_po_add  = purchase_order_detail_data_list.copy()
    # new_sub_total = 0
    # print(purchase_order_detail_data_list_for_po_add,"purchase Order Detail data list for po add")
    for purchase_order_detail_data_list_for_po in purchase_order_detail_data_list_for_po_add:
        try:
            purchase_order_main = PurchaseOrderMain.objects.get(purchase_order_type=1, supplier=purchase_order_detail_data_list_for_po['supplier'])
            purchase_order_detail_data_list_for_po.pop('supplier')
            purchase_order_detail_serializer = CreatePurchaseOrderDetail(data=purchase_order_detail_data_list_for_po)
            if purchase_order_detail_serializer.is_valid(raise_exception=True):
                purchase_order_detail_serializer.save(purchase_order_main = purchase_order_main,
                created_by=current_user.get_created_by({'request': request}), created_date_ad=timezone.now())
            # new_sub_total+=purchase_order_main.total_amount
            # new_sub_total+=Decimal(purchase_order_detail_data_list_for_po['net_amount'])
            purchase_order_main.total_amount += Decimal(purchase_order_detail_serializer.data['net_amount'])
            purchase_order_detail_data_list.remove(purchase_order_detail_data_list_for_po)
            # added statically total amount = 0
        
            data= {
            "total_amount":0
            }
            print(data)
            purchase_order_main_serializer = CreatePurchaseOrderMain(purchase_order_main, data=data, partial=True)
            
            if purchase_order_main_serializer.is_valid(raise_exception=True):
                        purchase_order_main_serializer.save()
                        # print(purchase_order_main_serializer.data, "purchase order main data")
        except ObjectDoesNotExist as e:
            pass

    
    suppliers_ids = [a_dict['supplier'] for a_dict in purchase_order_detail_data_list]
    suppliers_ids = list(dict.fromkeys(suppliers_ids))
  
    for supplier_id in suppliers_ids:
        search_list = False
        if supplier_id is None:
            search_list = True
        purchase_order_main = {
            "purchase_order_type": 1,
            # "customer_order_main": customer_order_data['id'],
            "supplier": supplier_id,
            "total_amount": Decimal('0.00'),
            "purchase_order_details": [], 
            "search_list": search_list
           
        }
        for purchase_order_detail_data in purchase_order_detail_data_list:
            if(supplier_id==purchase_order_detail_data['supplier']):
                purchase_order_detail = purchase_order_detail_data.copy()
                purchase_order_detail.pop("supplier")
                purchase_order_main["purchase_order_details"].append(purchase_order_detail)
                # purchase_order_main["total_amount"] += Decimal(purchase_order_detail_data["net_amount"])
                # added statically total amount = 0
                purchase_order_main["total_amount"] = 0
        
        purchase_order_data_list.append(purchase_order_main)
    
    #Saving all data
    for purchase_order_data in purchase_order_data_list:
        purchase_order_data["purchase_order_no"] = custom_seq_generator.generate_purchase_order_no()
        serializer = CreatePurchaseOrderSerializer(data=purchase_order_data, context={'request': request})
        if(serializer.is_valid(raise_exception=True)):
            serializer.save()

         

class CreatePurchaseOrderDetail(serializers.ModelSerializer):
    class Meta: 
        model = PurchaseOrderDetail
        exclude = ['purchase_order_main']
        read_only_fields = ['created_date_ad', 'created_date_bs', 'created_by']


class CreatePurchaseOrderMain(serializers.ModelSerializer):
      class Meta: 
        model = PurchaseOrderMain
        fields= ['total_amount']
        read_only_fields = ['created_date_ad', 'created_date_bs', 'created_by']


class CreatePurchaseOrderSerializer(serializers.ModelSerializer):

    purchase_order_details = CreatePurchaseOrderDetail(many=True)
    class Meta:
        model = PurchaseOrderMain
        fields = "__all__"
        read_only_fields = ['created_date_ad', 'created_date_bs', 'created_by']
    
    

    def create(self, validated_data):   
        '''
        create method for Save customer order
        '''
        order_details = validated_data.pop('purchase_order_details')
        date_now = timezone.now()
        
        if not order_details:
            raise serializers.ValidationError("Please provide at least one order detail")
        validated_data['created_by'] = current_user.get_created_by(self.context)  
        order_main = PurchaseOrderMain.objects.create(**validated_data, created_date_ad=date_now)
        for order_detail in order_details:
              PurchaseOrderDetail.objects.create(**order_detail, purchase_order_main = order_main, created_by =validated_data['created_by'],
                                created_date_ad=date_now)   
              
        return order_main



def update_po_co_canceld(customer_order_id):
    canceled_customer_order_details = OrderDetail.objects.filter(order=customer_order_id)
    for canceled_customer_order_detail in canceled_customer_order_details:
        try:
            purchase_order_detail = PurchaseOrderDetail.objects.filter(available=1).get(item=canceled_customer_order_detail.item)
            if purchase_order_detail.qty > canceled_customer_order_detail.qty:
                new_po_qty = purchase_order_detail.qty - canceled_customer_order_detail.qty
                new_sub_total = new_po_qty * purchase_order_detail.amount
                new_discount_amount = Decimal(new_sub_total * purchase_order_detail.discount_rate / 100).quantize(quantize_places)
                new_net_amount = new_sub_total - new_discount_amount
                # net_amount_difference  = purchase_order_detail.net_amount - new_net_amount

                #saving to db
                purchase_order_detail.qty = new_po_qty
                purchase_order_detail.sub_total = new_sub_total
                purchase_order_detail.discount_amount = new_discount_amount
                purchase_order_detail.net_amount = new_net_amount
                purchase_order_detail.save()
                purchase_order_main = purchase_order_detail.purchase_order_main
                # purchase_order_main.total_amount = purchase_order_main.total_amount - net_amount_difference
                # added statically total amount =0 
                purchase_order_main.total_amount = 0
                purchase_order_main.save()
            else:
                purchase_order_detail.available = 4
                purchase_order_detail.save()
                purchase_order_main = purchase_order_detail.purchase_order_main
                # purchase_order_main.total_amount = purchase_order_main.total_amount - purchase_order_detail.net_amount
                # added statically total amount = 0
                purchase_order_main.total_amount = 0
                purchase_order_main.save()
        except ObjectDoesNotExist:
            pass


def update_po_detail_co_canceld(customer_order_detail_id):
    canceled_customer_order_detail = OrderDetail.objects.get(id=customer_order_detail_id)

    try:
            purchase_order_detail = PurchaseOrderDetail.objects.filter(available=1).get(item__id=canceled_customer_order_detail.item.id)
            print(purchase_order_detail, "this is ")
            # print('po pending qty (should be 3): ', purchase_order_detail.qty)
            # print('co cancel qty (should be 4/0): ', canceled_customer_order_detail.qty)

            if purchase_order_detail.qty > canceled_customer_order_detail.qty:
                print("if")
                new_po_qty = purchase_order_detail.qty - canceled_customer_order_detail.qty
                new_sub_total = new_po_qty * purchase_order_detail.amount
                new_discount_amount = Decimal(new_sub_total * purchase_order_detail.discount_rate / 100).quantize(quantize_places)
                new_net_amount = new_sub_total - new_discount_amount
                # net_amount_difference  = purchase_order_detail.net_amount - new_net_amount

                # saving to db
                purchase_order_detail.qty = new_po_qty
                purchase_order_detail.sub_total = new_sub_total
                purchase_order_detail.discount_amount = new_discount_amount
                purchase_order_detail.net_amount = new_net_amount
                purchase_order_detail.save()
                purchase_order_main = purchase_order_detail.purchase_order_main
                # purchase_order_main.total_amount = purchase_order_main.total_amount - net_amount_difference
                # added statically total amount = 0
                purchase_order_main.total_amount = 0
                purchase_order_main.save()
            else:
                print("else")
                purchase_order_detail.available = 4 
                purchase_order_detail.save()
                purchase_order_main = purchase_order_detail.purchase_order_main
                # purchase_order_main.total_amount = purchase_order_main.total_amount - purchase_order_detail.net_amount
                # added statically total amount = 0
                purchase_order_main.total_amount = 0
                purchase_order_main.save()
    except ObjectDoesNotExist:
        pass
