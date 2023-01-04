
from decimal import Decimal
from src.purchase_order.models import  PurchaseOrderDetail, PurchaseOrderReceivedDetail
from django.core.exceptions import ObjectDoesNotExist


from decimal import Decimal
from src.item.models import PoPriority, Item
from .models import PurchaseOrderDetail, PurchaseOrderMain, PurchaseOrderReceivedDetail
from src.customer_order.models import OrderDetail
from django.utils import timezone
from src.custom_lib.functions import current_user
from rest_framework import serializers
from src.custom_lib.functions import custom_seq_generator
from django.core.exceptions import ObjectDoesNotExist
from src.custom_lib.functions.stock import get_item_customer_order_qty_all, get_item_pending_customer_order_qty_for_create_po_without_cod, get_pending_purchase_order, get_remaining_qty_of_item,get_purchase_order_unverified_qty, get_item_pending_customer_order_qty



quantize_places = Decimal(10) ** -2
def update_po_detail_delete_purchase_received(purchase_order_received_detail_id, request, supplier_priority: int):
    print("delete purchase rec verified method calling")
    purchase_order_received_detail = PurchaseOrderReceivedDetail.objects.get(id=purchase_order_received_detail_id)
    quantize_places = Decimal(10) ** -2
    purchase_order_data_list = []
    purchase_order_detail_data_list = []

    try:
        order_details=OrderDetail.objects.filter(item = purchase_order_received_detail.item.id, archived=False, cancelled=False)  

        for order_detail in order_details:
            order_details_archived=order_detail.archived
        
        if  order_details_archived==False:
            
            try:
                    company_id = Item.objects.get(id= purchase_order_received_detail.item.id).company.id
                    supplier_id = PoPriority.objects.filter(company=company_id, priority=supplier_priority).values_list("supplier", flat=True)[0]
            except Exception as e:
                    supplier_id = None
        
            if  purchase_order_received_detail.item_unit is None or purchase_order_received_detail.item_unit =="":
                item_unit = None
            else:
                item_unit =  purchase_order_received_detail.item_unit.id
                    
            stock_of_item = get_remaining_qty_of_item (purchase_order_received_detail.item) 
            stock_of_item = stock_of_item +get_purchase_order_unverified_qty(purchase_order_received_detail.item)
            # stock_of_item = stock_of_item + get_pending_purchase_order(purchase_order_received_detail.item)
            stock_of_item -= get_item_pending_customer_order_qty_for_create_po_without_cod(purchase_order_received_detail.item)
            # print(stock_of_item, " this is stock")
          
            if (Decimal(purchase_order_received_detail.qty) > stock_of_item):
                # print("this is condition match")
                if stock_of_item <= 0:
                    #    print("stock less than condition match")
                       purchase_qty = get_item_pending_customer_order_qty_for_create_po_without_cod(purchase_order_received_detail.item)- (get_purchase_order_unverified_qty(purchase_order_received_detail.item)+ get_remaining_qty_of_item (purchase_order_received_detail.item))
                       purchase_qty= purchase_qty - get_pending_purchase_order(purchase_order_received_detail.item)
                       print(purchase_qty, "this is po raise qty")
                elif get_purchase_order_unverified_qty(purchase_order_received_detail.item) >  get_item_pending_customer_order_qty_for_create_po_without_cod(purchase_order_received_detail.item):
                        pass

                else:
                    purchase_qty = Decimal(purchase_order_received_detail.qty)
                    # print('this is condition')

                sub_total = Decimal(str(purchase_qty * Decimal(purchase_order_received_detail.amount))).quantize(quantize_places)
                discount_amount = Decimal(str(sub_total * Decimal((purchase_order_received_detail.discount_rate)) / 100)).quantize(quantize_places)
                net_amount=(Decimal(sub_total - discount_amount))
            
                purchase_order_detail_data_list.append({
                    "available": 1,
                    "item": purchase_order_received_detail.item.id,
                    "qty":purchase_qty,
                    "item_unit": item_unit,
                    "discount_rate": purchase_order_received_detail.discount_rate,
                    "discount_amount": discount_amount,
                    "net_amount":  net_amount,
                    "amount": purchase_order_received_detail.amount,
                    "sub_total":  sub_total,
                    "supplier": supplier_id
                    })

                purchase_order_append_data = purchase_order_detail_data_list.copy()
                
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
                            # added  statically total amount = 0
                            purchase_order_main_db.total_amount = 0
                            purchase_order_detail_db.save()
                            purchase_order_main_db.save()
                            purchase_order_detail_data_list.remove(purchase_order)
                        except ObjectDoesNotExist as e:
                            pass

                    
                purchase_order_detail_data_list_for_po_add  = purchase_order_detail_data_list.copy()
                
                for purchase_order_detail_data_list_for_po in purchase_order_detail_data_list_for_po_add:
                        try:
                            purchase_order_main = PurchaseOrderMain.objects.get(purchase_order_type=1, supplier=purchase_order_detail_data_list_for_po['supplier'])
                            purchase_order_detail_data_list_for_po.pop('supplier')
                            purchase_order_detail_serializer = CreatePurchaseOrderDetail(data=purchase_order_detail_data_list_for_po)
                            if purchase_order_detail_serializer.is_valid(raise_exception=True):
                                purchase_order_detail_serializer.save(purchase_order_main = purchase_order_main,
                                created_by= purchase_order_received_detail.created_by, created_date_ad=timezone.now())
                            # purchase_order_main.total_amount += Decimal(purchase_order_detail_serializer.data['net_amount'])
                            # added statically total amount = 0
                            purchase_order_main.total_amount = 0
                            purchase_order_detail_data_list.remove(purchase_order_detail_data_list_for_po)
                        except ObjectDoesNotExist as e:
                            pass
                    

                for purchase_order_data in purchase_order_data_list:
                        purchase_order_data["purchase_order_no"] = custom_seq_generator.generate_purchase_order_no()
                        serializer = CreatePurchaseOrderSerializer(data=purchase_order_data, context={'request': request})
                        if(serializer.is_valid(raise_exception=True)):
                            serializer.save()

    except Exception as e:
        order_details= None



class CreatePurchaseOrderDetail(serializers.ModelSerializer):
    class Meta: 
        model = PurchaseOrderDetail
        exclude = ['purchase_order_main']
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