from decimal import Decimal
from rest_framework import serializers
from src.purchase_order.models import PurchaseOrderMain, PurchaseOrderDetail
from src.custom_lib.functions import custom_seq_generator
from src.item.models import Item, PoPriority
from django.utils import timezone
from src.custom_lib.functions import current_user
from django.core.exceptions import ObjectDoesNotExist
from src.custom_lib.functions.stock import get_item_pending_customer_order_qty_for_create_po_without_cod, get_pending_purchase_order, get_remaining_qty_of_item,get_purchase_order_unverified_qty, get_item_pending_customer_order_qty
from src.customer_order.models import OrderDetail


quantize_places = Decimal(10) ** -2
def  update_purchase_order_direct_sale(sale_data, request, supplier_priority: int):
   
    #print(customer_order_data)
    purchase_order_data_list = []
    purchase_order_detail_data_list = []
    sale_details = sale_data['sale_details']
    

    for sale_detail in sale_details:
        sale_item = sale_detail['item']
        sale_qty =  sale_detail['qty']
        stock_of_item = get_remaining_qty_of_item(sale_detail['item']) + get_purchase_order_unverified_qty(sale_detail['item'])
        # stock_of_item -= get_item_pending_customer_order_qty(sale_detail['item'])
        # print(stock_of_item, "stocks")
    
    try:
        order_details = OrderDetail.objects.filter(item = sale_item , order__delivery_status= 1, archived= False)       
    

        if sale_detail['ref_customer_order_detail'] is None:
            customer_order_qty =  get_item_pending_customer_order_qty_for_create_po_without_cod(sale_detail['item']) 
  

        try:
                company_id = Item.objects.get(id= sale_detail['item']).company.id
                supplier_id = PoPriority.objects.filter(company=company_id, priority=supplier_priority).values_list("supplier", flat=True)[0]
        except Exception as e:
                supplier_id = None

        if  sale_detail['item_unit'] is None or sale_detail['item_unit'] =="":
                item_unit = None
        else:
            item_unit = sale_detail['item_unit']     

        remaining_qty =  stock_of_item  

        if customer_order_qty >  remaining_qty:
            if remaining_qty<=0:
                purchase_order_qty=sale_detail['qty']
            else: 
                purchase_order_qty = (customer_order_qty - remaining_qty)-get_pending_purchase_order(sale_detail['item'])
            sub_total = Decimal(str(purchase_order_qty* Decimal(sale_detail['amount']))).quantize(quantize_places)
            discount_amount = Decimal(str(sub_total * Decimal((sale_detail['discount_rate'])) / 100)).quantize(quantize_places)
            net_amount = sub_total - discount_amount

            
            purchase_order_detail_data_list.append({
                    "available": 1,
                    "item": sale_detail['item'],
                    "qty":  purchase_order_qty,
                    "item_unit": item_unit,
                    "discount_rate": sale_detail['discount_rate'],
                    "discount_amount":discount_amount,
                    "net_amount": sale_detail['net_amount'],
                    "amount": sale_detail['amount'],
                    "sub_total": sub_total,
                    "supplier": supplier_id
                })

            purchase_order_append_data = purchase_order_detail_data_list.copy()

            for purchase_order in purchase_order_append_data:
                try:
                    purchase_order_detail_db = PurchaseOrderDetail.objects.filter(available=1).get(item=purchase_order['item'])
                    print(purchase_order_detail_db)
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
                    #added statically total amount = 0
                    purchase_order_main_db.total_amount = 0
                    purchase_order_detail_db.save()
                    purchase_order_main_db.save()
                    purchase_order_detail_data_list.remove(purchase_order)
                except ObjectDoesNotExist as e:
                    pass
            # -------------------------------------------------------------------------
            #  add order to already existing purchase order with same supplier
            purchase_order_detail_data_list_for_po_add  = purchase_order_detail_data_list.copy()
        
            for purchase_order_detail_data_list_for_po in purchase_order_detail_data_list_for_po_add:
                try:
                    purchase_order_main = PurchaseOrderMain.objects.get(purchase_order_type=1, supplier=purchase_order_detail_data_list_for_po['supplier'])
                    purchase_order_detail_data_list_for_po.pop('supplier')
                    purchase_order_detail_serializer = CreatePurchaseOrderDetail(data=purchase_order_detail_data_list_for_po)
                    if purchase_order_detail_serializer.is_valid(raise_exception=True):
                        purchase_order_detail_serializer.save(purchase_order_main = purchase_order_main,
                        created_by=current_user.get_created_by({'request': request}), created_date_ad=timezone.now())
                    # purchase_order_main.total_amount += Decimal(purchase_order_detail_serializer.data['net_amount'])
                    #added statically total amount = 0
                    purchase_order_main.total_amount = 0
                    purchase_order_detail_data_list.remove(purchase_order_detail_data_list_for_po)
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
        else:
            pass 

    except:
        order_details= None    
                                 
                # else:
                    
                #         try:
                #                 company_id = Item.objects.get(id= sale_detail['item']).company.id
                #                 supplier_id = PoPriority.objects.filter(company=company_id, priority=supplier_priority).values_list("supplier", flat=True)[0]
                #         except Exception as e:
                #                 supplier_id = None

                #         if  sale_detail['item_unit'] is None or sale_detail['item_unit'] =="":
                #                 item_unit = None
                #         else:
                #             item_unit = sale_detail['item_unit']     

                #         stock_of_item = get_remaining_qty_of_item(sale_detail['item']) + get_purchase_order_unverified_qty(sale_detail['item'])
                #         stock_of_item -= get_item_pending_customer_order_qty(sale_detail['item'])

                            
                #         if (Decimal(sale_detail['qty']) > stock_of_item): 
                #                 # check if stock is in negative
                #                 if stock_of_item <=0:
                #                     sale_qty = Decimal(sale_detail['qty']) 
                #                 else:
                #                     sale_qty = Decimal(sale_detail['qty']) - Decimal(stock_of_item)

                #         sub_total = Decimal(str(sale_qty * Decimal(sale_detail['amount']))).quantize(quantize_places)
                #         discount_amount = Decimal(str(sub_total * Decimal((sale_detail['discount_rate'])) / 100)).quantize(quantize_places)
                #         net_amount = sub_total - discount_amount

                #         purchase_order_detail_data_list.append({
                #                     "available": 1,
                #                     "item": sale_detail['item'],
                #                     "qty":   sale_qty,
                #                     "item_unit": item_unit,
                #                     "discount_rate": sale_detail['discount_rate'],
                #                     "discount_amount":  discount_amount,
                #                     "net_amount": net_amount,
                #                     "amount": sale_detail['amount'],
                #                     "sub_total": sub_total,
                #                     "supplier": supplier_id
                #                 })

                #         purchase_order_append_data = purchase_order_detail_data_list.copy()

                #         for purchase_order in purchase_order_append_data:
                #                 try:
                #                     purchase_order_detail_db = PurchaseOrderDetail.objects.filter(available=1).get(item=purchase_order['item'])
                #                     print(purchase_order_detail_db)
                #                     purchase_order_main_db = purchase_order_detail_db.purchase_order_main
                #                     purchase_order_detail_db.qty += Decimal(purchase_order['qty'])
                #                     # sub total calculation and update
                #                     sub_total = Decimal(purchase_order['qty']) * purchase_order_detail_db.amount
                #                     sub_total =sub_total.quantize(quantize_places) # round off
                #                     purchase_order_detail_db.sub_total += sub_total # updated in detail

                #                     # net total calculation and update
                #                     discount_amount = sub_total * Decimal(purchase_order["discount_rate"]) / 100
                #                     discount_amount = discount_amount.quantize(quantize_places) # round off
                #                     purchase_order_detail_db.discount_amount += discount_amount

                #                     net_amount = sub_total - discount_amount
                #                     purchase_order_detail_db.net_amount += net_amount
                #                     # purchase_order_main_db.total_amount += net_amount
                #                     #added statically total amount = 0
                #                     purchase_order_main_db.total_amount = 0
                #                     purchase_order_detail_db.save()
                #                     purchase_order_main_db.save()
                #                     purchase_order_detail_data_list.remove(purchase_order)
                #                 except ObjectDoesNotExist as e:
                #                     pass
                #             # -------------------------------------------------------------------------
                #             #  add order to already existing purchase order with same supplier
                #         purchase_order_detail_data_list_for_po_add  = purchase_order_detail_data_list.copy()
                        
                #         for purchase_order_detail_data_list_for_po in purchase_order_detail_data_list_for_po_add:
                #                 try:
                #                     purchase_order_main = PurchaseOrderMain.objects.get(purchase_order_type=1, supplier=purchase_order_detail_data_list_for_po['supplier'])
                #                     purchase_order_detail_data_list_for_po.pop('supplier')
                #                     purchase_order_detail_serializer = CreatePurchaseOrderDetail(data=purchase_order_detail_data_list_for_po)
                #                     if purchase_order_detail_serializer.is_valid(raise_exception=True):
                #                         purchase_order_detail_serializer.save(purchase_order_main = purchase_order_main,
                #                         created_by=current_user.get_created_by({'request': request}), created_date_ad=timezone.now())
                #                     # purchase_order_main.total_amount += Decimal(purchase_order_detail_serializer.data['net_amount'])
                #                     #added statically total amount = 0
                #                     purchase_order_main.total_amount = 0
                #                     purchase_order_detail_data_list.remove(purchase_order_detail_data_list_for_po)
                #                 except ObjectDoesNotExist as e:
                #                     pass


                #         suppliers_ids = [a_dict['supplier'] for a_dict in purchase_order_detail_data_list]
                #         suppliers_ids = list(dict.fromkeys(suppliers_ids))
                        
                #         for supplier_id in suppliers_ids:
                #                 search_list = False
                #                 if supplier_id is None:
                #                     search_list = True
                #                 purchase_order_main = {
                #                     "purchase_order_type": 1,
                #                     "supplier": supplier_id,
                #                     "total_amount": Decimal('0.00'),
                #                     "purchase_order_details": [], 
                #                     "search_list": search_list
                                
                #                 }
                #                 for purchase_order_detail_data in purchase_order_detail_data_list:
                #                     if(supplier_id==purchase_order_detail_data['supplier']):
                #                         purchase_order_detail = purchase_order_detail_data.copy()
                #                         purchase_order_detail.pop("supplier")
                #                         purchase_order_main["purchase_order_details"].append(purchase_order_detail)
                #                         # purchase_order_main["total_amount"] += Decimal(purchase_order_detail_data["net_amount"])
                #                         # added statically total amount = 0
                #                         purchase_order_main["total_amount"] = 0
                                
                #                 purchase_order_data_list.append(purchase_order_main)
                            
                #         #Saving all data
                #         for purchase_order_data in purchase_order_data_list:
                #                 purchase_order_data["purchase_order_no"] = custom_seq_generator.generate_purchase_order_no()
                #                 serializer = CreatePurchaseOrderSerializer(data=purchase_order_data, context={'request': request})
                #                 if(serializer.is_valid(raise_exception=True)):
                #                     serializer.save()

          

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



quantize_places = Decimal(10) ** -2
def update_purchase_order_sale_return(sale_data):
    sale_details = sale_data['sale_details']
    for sale_detail in sale_details:
        try:
            purchase_order_detail = PurchaseOrderDetail.objects.filter(available=1).get(item=sale_detail['item'])
            if purchase_order_detail.qty > sale_detail['qty']:
                    new_po_qty = purchase_order_detail.qty - sale_detail['qty']
                    new_sub_total = new_po_qty * purchase_order_detail.amount
                    new_discount_amount = Decimal(new_sub_total * purchase_order_detail.discount_rate / 100).quantize(quantize_places)
                    new_net_amount = new_sub_total - new_discount_amount
                    # net_amount_difference  = purchase_order_detail.net_amount - new_net_amount
                    # print(new_net_amount )

                    #saving to db
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
                    purchase_order_detail.available = 4
                    purchase_order_detail.save()
                    purchase_order_main = purchase_order_detail.purchase_order_main
                    # purchase_order_main.total_amount = purchase_order_main.total_amount - purchase_order_detail.net_amount
                    # added statically total amount = 0
                    purchase_order_main.total_amount = 0
                    purchase_order_main.save()

        except  ObjectDoesNotExist:
            pass
