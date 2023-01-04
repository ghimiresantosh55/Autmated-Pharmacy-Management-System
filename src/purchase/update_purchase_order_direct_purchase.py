from decimal import Decimal
from src.customer_order.models import OrderDetail
from src.purchase_order.models import  PurchaseOrderDetail
from django.core.exceptions import ObjectDoesNotExist


quantize_places = Decimal(10) ** -2
def update_purchase_order_direct_purchase(purchase_data):
    purchase_details = purchase_data['purchase_details']
    print( "this is purchase detail data")
    for purchase_detail in purchase_details:
        try:
            purchase_order_detail = PurchaseOrderDetail.objects.filter(available=1).get(item=purchase_detail['item'])
            # print(purchase_order_detail.qty)
            # print(purchase_detail['qty'])
            if purchase_order_detail.qty > purchase_detail['qty']:
                    new_po_qty = purchase_order_detail.qty - purchase_detail['qty']
                    new_sub_total = new_po_qty * purchase_order_detail.amount
                    new_discount_amount = Decimal(new_sub_total * purchase_order_detail.discount_rate / 100).quantize(quantize_places)
                    #  # added statically total amount = 0
                    # new_net_amount = new_sub_total - new_discount_amount
                    # net_amount_difference  = purchase_order_detail.net_amount - new_net_amount
                   

                    #saving to db
                    purchase_order_detail.qty = new_po_qty
                    purchase_order_detail.sub_total = new_sub_total
                    purchase_order_detail.discount_amount = new_discount_amount
                    # added statically total amount = 0
                    # purchase_order_detail.net_amount = new_net_amount
                    purchase_order_detail.save()
                    purchase_order_main = purchase_order_detail.purchase_order_main
                     # added statically total amount = 0
                    # purchase_order_main.total_amount = purchase_order_main.total_amount - net_amount_difference
                   
                    purchase_order_main.total_amount=0
                    print(purchase_order_main.total_amount, "total amount direct purchase")
                    purchase_order_main.save()
            else:
                    purchase_order_detail.available = 4
                    purchase_order_detail.save()
                    purchase_order_main = purchase_order_detail.purchase_order_main
                    # added statically total amount = 0
                    # purchase_order_main.total_amount = purchase_order_main.total_amount - purchase_order_detail.net_amount
                    purchase_order_main.total_amount=0  
                    print(purchase_order_main.total_amount, "total amount direct purchase")   
                    purchase_order_main.save()

        except  ObjectDoesNotExist:
            pass




quantize_places = Decimal(10) ** -2
def update_purchase_order_save_opening_stock(purchase_data):
    purchase_details = purchase_data['purchase_details']
    for purchase_detail in purchase_details:
        try:
            purchase_order_detail = PurchaseOrderDetail.objects.filter(available=1).get(item=purchase_detail['item'])
            if purchase_order_detail.qty > purchase_detail['qty']:
                    new_po_qty = purchase_order_detail.qty - purchase_detail['qty']
                    new_sub_total = new_po_qty * purchase_order_detail.amount
                    new_discount_amount = Decimal(new_sub_total * purchase_order_detail.discount_rate / 100).quantize(quantize_places)
                    new_net_amount = new_sub_total - new_discount_amount
                     # added statically total amount = 0
                    # net_amount_difference  = purchase_order_detail.net_amount - new_net_amount
                    # print(new_net_amount )

                    #saving to db
                    purchase_order_detail.qty = new_po_qty
                    purchase_order_detail.sub_total = new_sub_total
                    purchase_order_detail.discount_amount = new_discount_amount
                    purchase_order_detail.net_amount = new_net_amount
                    purchase_order_detail.save()
                    purchase_order_main = purchase_order_detail.purchase_order_main
                        # added statically total amount = 0
                    # purchase_order_main.total_amount = purchase_order_main.total_amount - net_amount_difference
                    purchase_order_main.total_amount =0
                    print(purchase_order_main.total_amount)
                    purchase_order_main.save()
            else:
                    purchase_order_detail.available = 4
                    purchase_order_detail.save()
                    purchase_order_main = purchase_order_detail.purchase_order_main
                    # added statically total amount = 0
                    # purchase_order_main.total_amount = purchase_order_main.total_amount - purchase_order_detail.net_amount
                    purchase_order_main.total_amount = 0
                    print(purchase_order_main.total_amount, "total amount direct purchase")
                    purchase_order_main.save()

        except  ObjectDoesNotExist:
            pass
