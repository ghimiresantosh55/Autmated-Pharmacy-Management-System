from rest_framework import serializers
from src.custom_lib.functions.stock import get_remaining_qty_of_purchase, get_remaining_qty_of_item
from src.purchase.models import PurchaseDetail

def update_purchase_for_sale(sale_details):

    if not sale_details:
        serializers.ValidationError("Please provide at least one sale detail")

    #  create sale detail purchase wise
    return_data_sale_details = []
   
    for sale_detail in sale_details:
        item_id = sale_detail['item'].id
        given_qty = sale_detail['qty']
        remaining_qty = get_remaining_qty_of_item(item_id=item_id)
        if given_qty > remaining_qty:
           raise serializers.ValidationError({"sale_detail": f"item qty greater than stock qty for {sale_detail['item'].brand_name}"})
        


    for sale_detail in sale_details:
        item_id = sale_detail['item'].id
        sale_qty = sale_detail['qty']
        purchase_details_for_item = PurchaseDetail.objects.filter(item=item_id).order_by("id")
        for purchase_detail in purchase_details_for_item:
        
            remaining_qty_purchase = get_remaining_qty_of_purchase(purchase_detail.id)
            if remaining_qty_purchase > 0:
                if sale_qty <= remaining_qty_purchase:
                    sale_detail_data = {
                        "item": sale_detail['item'],
                        "qty": sale_qty,
                        "item_unit": sale_detail['item_unit'],
                        "amount": sale_detail['amount'],
                        "discount_rate": sale_detail['discount_rate'],
                        "discount_amount": sale_qty*sale_detail['amount']*sale_detail['discount_rate']/100,
                        "sub_total": sale_qty *  sale_detail['amount'],
                        "net_amount": (sale_qty *  sale_detail['amount'])-(sale_qty*sale_detail['amount']*sale_detail['discount_rate']/100),
                        "ref_purchase_detail": purchase_detail,
                        "ref_customer_order_detail":sale_detail['ref_customer_order_detail'],
                    
                    }
                    return_data_sale_details.append(sale_detail_data)
                    break
                else:
                    sale_detail_data = {
                        "item": sale_detail['item'],
                        "qty": remaining_qty_purchase,
                        "item_unit": sale_detail['item_unit'],
                        "amount": sale_detail['amount'],
                        "discount_rate": sale_detail['discount_rate'],
                        "discount_amount": remaining_qty_purchase*sale_detail['amount']*sale_detail['discount_rate']/100,
                        "sub_total": remaining_qty_purchase *  sale_detail['amount'],
                        "net_amount": (remaining_qty_purchase *  sale_detail['amount'])-(remaining_qty_purchase*sale_detail['amount']*sale_detail['discount_rate']/100),
                        "ref_purchase_detail": purchase_detail,
                        "ref_customer_order_detail":sale_detail['ref_customer_order_detail'],
                    
                    }
                    return_data_sale_details.append(sale_detail_data)

                sale_qty -= remaining_qty_purchase
    # print(return_data_sale_details, "this is sale details")
    return return_data_sale_details