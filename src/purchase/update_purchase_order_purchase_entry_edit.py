from decimal import Decimal
from src.purchase_order.models import  PurchaseOrderDetail, PurchaseOrderReceivedDetail
from src.purchase.models import PurchaseDetail
from django.core.exceptions import ObjectDoesNotExist
from decimal import Decimal
from src.item.models import PoPriority, Item
from src.purchase_order.models import PurchaseOrderDetail, PurchaseOrderMain
from django.utils import timezone
from src.custom_lib.functions import current_user
from rest_framework import serializers
from src.custom_lib.functions import custom_seq_generator
from django.core.exceptions import ObjectDoesNotExist
from functools import reduce
from src.customer_order.models import OrderDetail
from src.custom_lib.functions.stock import get_remaining_qty_of_item, get_purchase_order_unverified_qty, get_item_pending_customer_order_qty



quantize_places = Decimal(10) ** -2
def  update_po_detail_edit_purchase_entry(purchase_order_received_data, purchase_data, request, supplier_priority: int):
    # print("hello this function is calling")
    purchase_order_data_list = []
    purchase_order_detail_data_list = []

    purchase_order_received_details = purchase_order_received_data['purchase_order_received_details']
    purchase_details = purchase_data['purchase_details']

    purchase_received_detail_diff=[]
    purchase_detail_diff= []

    for purchase_received_detail in purchase_order_received_details:
        purchase_received_detail =  dict(purchase_received_detail)

        purchase_received_detail_diff.append(purchase_received_detail)
    # print( purchase_received_detail_diff)
   

    for purchase in purchase_details:
        purchase =  dict(purchase)
        if purchase['ref_purchase_order_received_detail'] is not None:
            purchase_detail_diff.append(purchase)
      

    # Listing for purchase order received item which is not verified
    purchase_received_diff_item = []
    for item in purchase_received_detail_diff:
        for detail in  purchase_detail_diff:
            if item['item']!= detail['item']:
                purchase_received_diff_item.append(item)
       
            

    #Listing with newly added verify items and received order items
    purchase_detail_ref_not_null = []
    purchase_detail_ref_null= []

    for purchase_detail in purchase_details:
        purchase_detail = dict(purchase_detail)
        
        if purchase_detail['ref_purchase_order_received_detail'] == "" or  purchase_detail['ref_purchase_order_received_detail'] == None:
            purchase_detail_ref_null.append(purchase_detail)

        else:
             purchase_detail_ref_not_null.append(purchase_detail)
    

    common_received_detail=[]
    common_purchase_detail= []
    for received_detail in purchase_order_received_details:
        # print(received_detail, "this is purchase received detail")
        
        for detail in purchase_details:
            # print(detail, "this is purchase detail")
            if received_detail['item']==detail['item']:
                common_received_detail.append(received_detail)
                common_purchase_detail.append(detail)

    not_equal_item = []
    for received_detail in purchase_order_received_details:
        # print(received_detail['archived'], "received detail")
        if received_detail not in common_received_detail:
                not_equal_item.append(received_detail)

    
    for i in  range(len(common_received_detail)):
                # print("common item is calling")
                purchase_order_received_detail= common_received_detail[i-1]
                purchase_detail= common_purchase_detail[i-1]
                purchase_order_received_ref_id = purchase_order_received_detail['ref_purchase_order_received_detail'] 
                purchase_received_detail_data =  PurchaseOrderReceivedDetail.objects.get(id = purchase_order_received_ref_id)
                # print(purchase_received_detail_data, " this is new item data")
                purchase_received_qty = purchase_received_detail_data.qty
                purchase_received_item = purchase_received_detail_data.item
                purchase_qty = purchase_detail['qty']
                purchase_item_data = purchase_detail['id']
                purchase_item_id =  PurchaseDetail.objects.get(id = purchase_item_data)
                purchase_item = purchase_item_id.item
                # this condition check if received order item and verify item.
                if purchase_received_item==purchase_item:     
                    #this will check if verify quantity is greater than purchase order received item.
                    if  purchase_qty > purchase_received_qty:
                                # print("this condition running 1 which is common item")
                              
                                try:
                                    purchase_order_detail = PurchaseOrderDetail.objects.filter(available=1).get(item=purchase_detail['item']) 
                                    difference_qty =  purchase_qty - purchase_received_qty

                                   
                                    if  difference_qty >= purchase_order_detail.qty:
                                        purchase_order_detail.available = 4
                                        purchase_order_detail.save()
                                        purchase_order_main = purchase_order_detail.purchase_order_main
                                        # purchase_order_main.total_amount = purchase_order_main.total_amount - purchase_order_detail.net_amount
                                        # added statically total amount = 0
                                        purchase_order_main.total_amount = 0
                                        purchase_order_main.save()

                                    else:          
                                        new_po_qty = purchase_order_detail.qty - difference_qty
                                        new_sub_total = new_po_qty * purchase_order_detail.amount
                                        new_discount_amount = Decimal(new_sub_total * purchase_order_detail.discount_rate / 100).quantize(quantize_places)
                                        new_net_amount = new_sub_total - new_discount_amount
                                        # net_amount_difference  = purchase_order_detail.net_amount - new_net_amount

                                        #saving to db
                                        purchase_order_detail.qty = new_po_qty
                                        # print(purchase_order_detail.qty, "new po qty of 80")
                                        purchase_order_detail.sub_total = new_sub_total
                                        purchase_order_detail.discount_amount = new_discount_amount
                                        purchase_order_detail.net_amount = new_net_amount
                                        # print(new_net_amount, "new net amount")
                                        purchase_order_detail.save()
                                        purchase_order_main = purchase_order_detail.purchase_order_main
                                        # purchase_order_main.total_amount = purchase_order_main.total_amount - net_amount_difference
                                         # added statically total amount = 0
                                        purchase_order_main.total_amount = 0
                                        # print(purchase_order_main.total_amount, "purchase order total amount")
                                        purchase_order_main.save()    

                                except  ObjectDoesNotExist:
                                       pass 

                    
                    elif purchase_qty < purchase_received_qty:
                                    # print("this condition running 2")
                                   # this condition will check verify quantity is lesser than received quantity or not
                                    difference_qty = purchase_received_qty - purchase_qty
                                    try:
                                        company_id = Item.objects.get(id= purchase_detail['item']).company.id
                                        supplier_id = PoPriority.objects.filter(company=company_id, priority=supplier_priority).values_list("supplier", flat=True)[0]
                                    except Exception as e:
                                        supplier_id = None

                                    if  purchase_detail['item_unit'] is None or  purchase_detail['item_unit'] =="":
                                        item_unit = None
                                    else:
                                        item_unit =  purchase_detail['item_unit']

                                        sub_total = Decimal(str(difference_qty * Decimal(purchase_detail['amount']))).quantize(quantize_places)
                                        discount_amount = Decimal(str(sub_total * Decimal((purchase_detail['discount_rate'])) / 100)).quantize(quantize_places)
                                        net_amount = sub_total - discount_amount

                                        purchase_order_detail_data_list.append({
                                            "available": 1,
                                            "item": purchase_detail['item'],
                                            "qty": difference_qty,
                                            "item_unit": item_unit,
                                            "discount_rate": purchase_detail['discount_rate'],
                                            "discount_amount": discount_amount,
                                            "net_amount": net_amount,
                                            "amount": purchase_detail['amount'],
                                            "sub_total": sub_total,
                                            "supplier": supplier_id
                                            })
                                        purchase_order_append_data = purchase_order_detail_data_list.copy()
                                        # print(purchase_order_append_data )
                                        for purchase_order in purchase_order_append_data:
                                            try:
                                                purchase_order_detail_db = PurchaseOrderDetail.objects.filter(available=1).get(item=purchase_order['item'])
                                                purchase_order_main_db = purchase_order_detail_db.purchase_order_main
                                                # print(purchase_order['qty'], " this is be added qty in po")
                                                # print(purchase_order_detail_db.qty, " this is db qty")
                                                purchase_order_detail_db.qty += Decimal(purchase_order['qty'])
                                                # print(purchase_order_detail_db.qty, " this is item ")
                                                   
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
                                                #  purchase_order_main.total_amount += Decimal(purchase_order_detail_serializer.data['net_amount'])
                                                # added statically total amount = 0
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

                else:
                    pass    

                                             
    if len(purchase_detail_ref_null) > 0:
        # print("null is running")
        # this condition  will check reference purchase received id null. thats means new item is added to verify process.
        for purchase_detail in purchase_detail_ref_null:
            
                try:         
                        purchase_order_detail = PurchaseOrderDetail.objects.filter(available=1).get(item=purchase_detail['item'])
                        if purchase_order_detail.qty > purchase_detail['qty']:
                            new_po_qty = purchase_order_detail.qty - purchase_detail['qty']
                            new_sub_total = new_po_qty * purchase_order_detail.amount
                            new_discount_amount = Decimal(new_sub_total * purchase_order_detail.discount_rate / 100).quantize(quantize_places)
                            new_net_amount = new_sub_total - new_discount_amount
                            # net_amount_difference  = purchase_order_detail.net_amount - new_net_amount

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
                             # added statically total amount = 0
                            # purchase_order_main.total_amount = purchase_order_main.total_amount - purchase_order_detail.net_amount
                            purchase_order_main.total_amount = 0
                            purchase_order_main.save()

                except ObjectDoesNotExist:
                        pass
                    
    if len(not_equal_item)> 0: 
        # print("not null is running")
        
        #this condition will check purchase received item which is not in verify.
        for purchase_order_received_detail in not_equal_item:

            try:
                purchase_order_received_details= PurchaseOrderReceivedDetail.objects.filter(item = purchase_order_received_detail['item'], archived = True)
            except:
             
                try:
                    company_id = Item.objects.get(id= purchase_order_received_detail['item']).company.id
                    supplier_id = PoPriority.objects.filter(company=company_id, priority=supplier_priority).values_list("supplier", flat=True)[0]
                except Exception as e:
                    supplier_id = None

                if  purchase_order_received_detail['item_unit'] is None or  purchase_order_received_detail['item_unit'] =="":
                    item_unit = None
                else:
                        item_unit =  purchase_order_received_detail['item_unit']

                        purchase_qty = Decimal(purchase_order_received_detail['qty'])
                        print(purchase_qty,"not equal item case po raise qty running")
                        sub_total = Decimal(str(purchase_qty * Decimal( purchase_order_received_detail['amount']))).quantize(quantize_places)
                        discount_amount = Decimal(str(sub_total * Decimal(( purchase_order_received_detail['discount_rate'])) / 100)).quantize(quantize_places)
                        net_amount = sub_total - discount_amount

                        purchase_order_detail_data_list.append({
                            "available": 1,
                            "item":   purchase_order_received_detail['item'],
                            "qty":   purchase_qty,
                            "item_unit": item_unit,
                            "discount_rate":  purchase_order_received_detail['discount_rate'],
                            "discount_amount": discount_amount,
                            "net_amount": net_amount,
                            "amount": purchase_order_received_detail['amount'],
                            "sub_total": sub_total,
                            "supplier": supplier_id
                                })
                        purchase_order_append_data = purchase_order_detail_data_list.copy()
            
                        for purchase_order in purchase_order_append_data:
                            try:
                                purchase_order_detail_db = PurchaseOrderDetail.objects.filter(available=1).get(item=purchase_order['item'])
                                purchase_order_main_db = purchase_order_detail_db.purchase_order_main
                                purchase_order_detail_db.qty += Decimal(purchase_order['qty'])
                                sub_total = Decimal(purchase_order['qty']) * purchase_order_detail_db.amount
                                sub_total =sub_total.quantize(quantize_places) # round off
                                purchase_order_detail_db.sub_total += sub_total # updated in detail

                                #net total calculation and update
                                discount_amount = sub_total * Decimal(purchase_order["discount_rate"]) / 100
                                discount_amount = discount_amount.quantize(quantize_places) # round off
                                purchase_order_detail_db.discount_amount += discount_amount

                                net_amount = sub_total - discount_amount
                                purchase_order_detail_db.net_amount += net_amount
                                # purchase_order_main_db.total_amount += net_amount
                                # added statically total amount = 0
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
                                    created_by=current_user.get_created_by({'request': request}), created_date_ad=timezone.now())
                                # added statically total amount = 0
                                #   purchase_order_main.total_amount += Decimal(purchase_order_detail_serializer.data['net_amount'])
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
                                    #added statically total amount = 0
                                    purchase_order_main["total_amount"] = 0
                            
                            purchase_order_data_list.append(purchase_order_main)


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
