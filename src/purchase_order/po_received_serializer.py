from decimal import Decimal
from rest_framework import serializers
from src.company.models import Company
from src.item.models import Item, ItemUnit, PoPriority
from src.supplier.models import Supplier
from src.company.models import Company
from .models import PurchaseOrderDetail, PurchaseOrderMain, PurchaseOrderReceivedDetail, PurchaseOrderReceivedMain
from django.utils import timezone
from src.custom_lib.functions import current_user
from .purchase_order_unique_id_generator import generate_purchase_order_received_no
from src.custom_lib.functions import custom_seq_generator
from django.core.exceptions import ObjectDoesNotExist
from src.customer_order.models import OrderDetail
from django.db.models import Exists, OuterRef, Q

class ReceivedDataSerializer(serializers.Serializer):
    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.filter(active=True))
    qty = serializers.DecimalField(max_digits=12, decimal_places=2)
    item_unit = serializers.PrimaryKeyRelatedField(queryset=ItemUnit.objects.filter(active=True), allow_null = True)
    discount_rate = serializers.DecimalField(max_digits=12, decimal_places=2)
    discount_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    net_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    sub_total = serializers.DecimalField(max_digits=12, decimal_places=2)
    purchase_order_detail =  serializers.PrimaryKeyRelatedField(queryset=PurchaseOrderDetail.objects.filter(available=1), allow_null = True)



class SaveCustomerOrderReceivedSerializer(serializers.Serializer):
    purchase_order_main = serializers.PrimaryKeyRelatedField(queryset=PurchaseOrderMain.objects.filter(purchase_order_type=1))
    supplier = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all(), allow_null=True)
    available = ReceivedDataSerializer(many=True)
    not_available = ReceivedDataSerializer(many=True)
    informed = ReceivedDataSerializer(many=True)
    remarks = serializers.CharField(default="", allow_blank = True)

    def create(self, validated_data):
        quantize_places = Decimal(10) ** -2
        date_now = timezone.now()
        created_by = current_user.get_created_by(self.context)
        # print("created by %%%%%%%%%%%%", self.context)
       
        
        if validated_data['available']:
            self.save_available(
                supplier=validated_data['supplier'],
                validated_data=validated_data['available'], 
                date_now=date_now, created_by=created_by, 
                purchase_order_main=validated_data['purchase_order_main'],
                remarks = validated_data['remarks']
            )
        if validated_data['not_available']:
            self.save_not_available(
                validated_data=validated_data['not_available'], 
                date_now=date_now, created_by=created_by, 
                purchase_order_main=validated_data['purchase_order_main'],
                supplier=validated_data.get('supplier', None),
                request=self.context.get('request')
            )
        if validated_data['informed']:
            self.save_informed(
                validated_data=validated_data['informed'], 
                date_now=date_now, created_by=created_by, 
                purchase_order_main=validated_data['purchase_order_main']
            )

        return validated_data
    
    def save_available(self, supplier, validated_data, date_now, created_by, purchase_order_main, remarks):
        
        quantize_places = Decimal(10) ** -2
        # print("created_by ********************************", created_by)
        receive_main_data = {
            "purchase_order_received_type": 1,
            "purchase_order_received_no": generate_purchase_order_received_no(1),
            "supplier":supplier,
            "total_amount":Decimal('0.00'),
            "remarks":remarks,
            "purchase_order_main": purchase_order_main,
            "created_date_ad": date_now,
            "created_by": created_by
        }
        
        # print(validated_data, "valid data")
        for data in validated_data:
            receive_main_data['total_amount'] += data['sub_total']
       

        purchase_order_received_main = PurchaseOrderReceivedMain.objects.create(**receive_main_data)

        not_available_po_data = []
      
        for data in validated_data:
        
            temp_discount_amount = data['discount_amount']
            temp_sub_amount = data['sub_total']
            data['discount_amount']= 0
            data['net_amount'] = Decimal(data['sub_total'])
            purchase_order_received_detail = PurchaseOrderReceivedDetail.objects.create(**data, created_by=created_by,
             created_date_ad=date_now, purchase_order_received_main=purchase_order_received_main)
            # print(purchase_order_received_detail,"this is values")
            # print(data['purchase_order_detail'],"print")
            try:
                data['purchase_order_detail'].available = 2
                data['purchase_order_detail'].save()
            
                if data['purchase_order_detail'].qty > purchase_order_received_detail.qty:
                    data['qty'] = data['purchase_order_detail'].qty - purchase_order_received_detail.qty
                    data['sub_total'] =  Decimal(Decimal(data['qty']) * Decimal(data['amount'])).quantize(quantize_places)
                    data['discount_amount'] = Decimal(temp_discount_amount).quantize(quantize_places)
                    # data['discount_amount'] = Decimal(0)
                    data['net_amount'] = Decimal(temp_sub_amount-data['discount_amount'])
                    not_available_po_data.append(data)
            except:
               
                if data['purchase_order_detail']==None:
                    # print(purchase_order_received_detail.item,"if")
                    try:         
                        purchase_order_detail = PurchaseOrderDetail.objects.filter(available=1).get(item=purchase_order_received_detail.item)
                        if purchase_order_detail.qty >  purchase_order_received_detail.qty:
                            new_po_qty = purchase_order_detail.qty -  purchase_order_received_detail.qty
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
                            #added statically total amount = 0
                            # purchase_order_main.total_amount = purchase_order_main.total_amount - purchase_order_detail.net_amount
                            purchase_order_main.total_amount = 0
                            purchase_order_main.save()

                    except ObjectDoesNotExist:
                        pass
            
           
        if not_available_po_data:
            self.save_not_available(
                validated_data=not_available_po_data, 
                date_now=date_now, created_by=created_by, 
                purchase_order_main=purchase_order_main,
                supplier=purchase_order_received_main.supplier,
                request=self.context.get('request')
            )
        
        return purchase_order_received_main
    
    def save_not_available(self, validated_data, supplier, date_now, created_by, purchase_order_main, request):
        """
        function to create purchase order from customer order data
        """
        quantize_places = Decimal(10) ** -2
        purchase_order_data_list = []
        purchase_order_detail_data_list = []
        # customer_order_details = customer_order_data['order_details']
        customer_order_details = validated_data

        for customer_order_detail in customer_order_details:
            customer_order_item_id = customer_order_detail['item'].id
            company_id= Item.objects.filter(id=customer_order_item_id).values_list('company',flat=True)
            # changing from queryset
            company_value_id= list(company_id)
                       
            
            if company_value_id[0] is not None:
                supplier_exist = True
            
                # print(supplier_priorities, "supplier priorities list")
                if supplier: 
                    # adding of try catch for no supplier PoPriority 
                    try:    
                       
                        supplier_priority = int(PoPriority.objects.get(company=company_value_id[0], supplier=supplier.id).priority) + 1
                     
                        # print(customer_order_details[0]['item'].company.id, " this is company id")
                    except Exception as e:
                        supplier_priority = None
                            
                else:
                    supplier_priority = (PoPriority.objects.get(company=company_value_id[0], supplier=purchase_order_main.supplier.id).priority + 1)
                   
            else:
                supplier_exist = False
      
        # for customer_order_detail in customer_order_details:
            # company_id = Item.objects.get(id=customer_order_detail['item']['id']).company.id
            
            if supplier_exist:
                try:
                    supplier_id = PoPriority.objects.filter(company=company_value_id[0], priority = supplier_priority).values_list("supplier", flat=True)[0]
                    
                except IndexError:
                    supplier_id = None
                   
            else:
                supplier_id = None
            
            # Validation if unit is blank in customer order
            if customer_order_detail['item_unit'] is None or customer_order_detail['item_unit']=="":
                item_unit = None
            else:
                item_unit = customer_order_detail['item_unit'].id
            purchase_order_detail_data_list.append({
                # "customer_order_detail": customer_order_detail['id'], 
                "available": 1,
                "item": customer_order_detail['item'].id,
                "qty": customer_order_detail['qty'],
                "item_unit": item_unit,
                "discount_rate": customer_order_detail['discount_rate'],
                "discount_amount": customer_order_detail['discount_amount'],
                "net_amount": customer_order_detail['net_amount'],
                "amount": customer_order_detail['amount'],
                "sub_total": customer_order_detail['sub_total'],
                "supplier": supplier_id
            })
            customer_order_detail['purchase_order_detail'].available=4
            customer_order_detail['purchase_order_detail'].save()
        # filtering item with pending purchase order and adding them directly to PO
        purchase_order_append_data = purchase_order_detail_data_list.copy()

        for purchase_order in purchase_order_append_data:
            try:
                purchase_order_detail_db = PurchaseOrderDetail.objects.filter(available=1).get(item=purchase_order['item'])
                purchase_order_main_db = purchase_order_detail_db.purchase_order_main
                purchase_order_detail_db.qty += Decimal(purchase_order['qty'])
                #sub total calculation and update
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
                # purchase_order_main.total_amount += Decimal(purchase_order_detail_serializer.data['net_amount'])
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
    
    
    def save_informed(self, validated_data, date_now, created_by, purchase_order_main):
        for data in validated_data:
            customer_order_details = OrderDetail.objects.filter(item=data["item"].id, order__delivery_status=1)
            for customer_order_detail in customer_order_details:
                customer_order_detail.informed = True
                customer_order_detail.save()

            data['purchase_order_detail'].informed = True
            data['purchase_order_detail'].available = 4
            data['purchase_order_detail'].save()



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