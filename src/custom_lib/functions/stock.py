from lib2to3 import refactor
from src.purchase.models import PurchaseDetail
from src.purchase_order.models import PurchaseOrderDetail, PurchaseOrderReceivedDetail, PurchaseOrderReceivedMain
from src.sale.models import SaleDetail
from src.customer_order.models import OrderDetail
from django.db.models import F, Q
from django.db.models import Case, Value, When
from django.db import models
from django.http import JsonResponse

"""____________________________stock analysis of purchase _______________________________________________________________"""

# remaining_quantity = total_purchase_quantity - return_purchase_quantity - sale_quantity + sale_return_qty
def get_remaining_qty_of_purchase(ref_id):
    stock = get_purchase_qty(ref_id) - get_purchase_return_qty(ref_id) - \
            get_purchase_sale_qty(ref_id) + get_purchase_sale_return_qty(ref_id)
    return stock


# call value id of PurchaseDetail
def get_purchase_qty(ref_id):
    total_purchase_qty = sum(PurchaseDetail.objects.filter(pk=ref_id).\
                             values_list('qty', flat=True))
    return total_purchase_qty

 
# call value ref_purchase_detail
def get_purchase_return_qty(ref_id):
    total_purchase_return_qty = sum(
        PurchaseDetail.objects.filter(ref_purchase_detail=ref_id)
            .values_list('qty', flat=True))
    return total_purchase_return_qty


# call value ref_purchase_detail
def get_purchase_sale_qty(ref_id):
    total_sale_qty = sum(
        SaleDetail.objects.filter(ref_purchase_detail=ref_id, sale_main__sale_type=1).values_list('qty', flat=True))
    return total_sale_qty


# call value ref_purchase_detail
def get_purchase_sale_return_qty(ref_id):
    total_sale_return_qty = sum(
        SaleDetail.objects.filter(ref_purchase_detail=ref_id, sale_main__sale_type=2).values_list('qty', flat=True))
    return total_sale_return_qty


def get_pending_purchase_order(item_id):
    pending_po_qty = sum(PurchaseOrderDetail.objects.filter(available=1, informed=False, item=item_id).values_list('qty', flat=True))
    # print("penidng (3)",pending_po_qty)
    return pending_po_qty


"""____________________________stock analysis of items _______________________________________________________________"""

# calculate remaining qty of an item
def get_remaining_qty_of_item(item_id):
    stock = get_purchase_qty_of_item(item_id) - \
            get_purchase_return_qty_of_item(item_id) - \
            get_sale_qty_of_item(item_id) + get_sale_return_qty_of_item(item_id)
    # print("stock qty (should be 3)", stock)
    return stock

# calculating of total purchase qty of an item
def get_purchase_qty_of_item(item_id):
    total_quantity = sum(
        PurchaseDetail.objects.filter(item=item_id, purchase_main__purchase_type__in=[1,3]).values_list('qty', flat=True))
    return total_quantity

# calculating of total purchase return of an item
def get_purchase_return_qty_of_item(item_id):
    total_purchase_return_qty = sum(
        PurchaseDetail.objects.filter(item=item_id, purchase_main__purchase_type=2).values_list('qty', flat=True))
    return total_purchase_return_qty

# calculating of total sale of an item (sale_type=1 (ie sale))
def get_sale_qty_of_item(item_id):
    total_sale_qty = sum(
        SaleDetail.objects.filter(item=item_id, sale_main__sale_type=1).values_list('qty', flat=True))
    return total_sale_qty

# calculating of total sale return of item (sale_type=2 (ie return))
def get_sale_return_qty_of_item(item_id):
    total_sale_return_qty = sum(
        SaleDetail.objects.filter(item=item_id, sale_main__sale_type=2).values_list('qty', flat=True))
    return total_sale_return_qty

def get_item_purchase_order_qty(item_id):
    total_po_qty  = sum(OrderDetail.objects.filter(item=item_id, order__delivery_status=1).values_list('qty', flat=True))
    return total_po_qty

def get_item_purchase_qty(item_id):
    total_purchase_qty  = sum(PurchaseDetail.objects.filter(item=item_id, purchase_main__purchase_type=1).values_list('qty', flat=True))
    return total_purchase_qty

def get_item_purchase_received_qty(item_id):
    total_purchase_received_qty  = sum(PurchaseOrderReceivedDetail.objects.filter(item=item_id, purchase_order_received_main__purchase_order_received_type=2).values_list('qty', flat=True))
    return total_purchase_received_qty

#for customer order auto po generation 
# def get_purchase_order_unverified_qty(item_id):
#     return sum(PurchaseOrderReceivedDetail.objects.filter(item=item_id, archived = False, purchase_order_received_main__purchase_order_received_type=1).exclude(
#         id__in= PurchaseOrderReceivedDetail.objects.filter(ref_purchase_order_received_detail=id).values_list('qty', flat=True))
#     )

def get_purchase_order_unverified_qty(item_id):
    purchase_order_unverified_qty =  sum(PurchaseOrderReceivedDetail.objects.filter(item=item_id, archived = False, 
    purchase_order_received_main__purchase_order_received_type=1).
    exclude(id__in=PurchaseOrderReceivedDetail.objects.filter(archived=False, ref_purchase_order_received_detail__isnull=False)
    .values("ref_purchase_order_received_detail"))
    .values_list('qty', flat=True))
    # print("unverified qty (should be 2)", purchase_order_unverified_qty)
    return purchase_order_unverified_qty

# def get_purchase_order_unverified_item_qty(item_id, current_purchase_order_received_detail_id):
#      return sum(PurchaseOrderReceivedDetail.objects.exclude(id=current_purchase_order_received_detail_id).filter(item=item_id,archived = False, purchase_order_received_main__purchase_order_received_type=1).values_list('qty', flat=True))

def get_pending_customer_order_qty(item_id, current_order_detail_id):
    pending_co_qty =  sum(OrderDetail.objects.exclude(id=current_order_detail_id).filter(item=item_id, order__delivery_status=1).values_list('qty', flat=True))
    # print("pendig co qty(0)", pending_co_qty)
    return pending_co_qty

def get_item_pending_customer_order_qty(item_id):
    return sum(OrderDetail.objects.filter(item=item_id, archived = False, order__delivery_status=1).values_list('qty', flat=True))

def get_item_pending_customer_order_qty_for_create_po(item_id, current_order_detail_id):
    pending_co_qty =  sum(OrderDetail.objects.exclude(id=current_order_detail_id).
    filter(item=item_id, archived = False, order__delivery_status=1).
    values_list('qty', flat=True))
    # print("pending co qty (0): ", pending_co_qty)
    return pending_co_qty

def get_item_pending_customer_order_qty_for_create_po_without_cod(item_id):
    pending_co_qty =  sum(OrderDetail.objects.
    filter(item=item_id, archived = False, order__delivery_status=1).
    values_list('qty', flat=True))
    # print("pending co qty (4): ", pending_co_qty)
    return pending_co_qty

def get_item_customer_order_qty_all(item_id):
    all_co_qty =  sum(OrderDetail.objects.
    filter(item=item_id).
    values_list('qty', flat=True))
    # print("pending co qty (4): ", pending_co_qty)
    return all_co_qty
"""_________________________________________ sale stock analysis ___________________________________________"""




# calculating of sale return
def get_sale_return_qty(sale_detail_id):
    stock = sum(SaleDetail.objects.filter(ref_sale_detail=sale_detail_id).values_list('qty', flat=True))
    return stock

# calculating of remaining qty
def get_sale_remaining_qty(sale_detail_id):
    total_qty = SaleDetail.objects.values_list('qty', flat=True).get(id=sale_detail_id)
    stock = total_qty - get_sale_return_qty(sale_detail_id)
    return stock


"""_______________________________________ Supplier stock analysis ________________________________________"""


# def get_purchase_item_qty_of_supplier(supplier_id):
#     qty = PurchaseDetail.objects.filter(purchase_main__supplier=supplier_id).


def get_item_ledger(filterset):
  
    query = PurchaseDetail.objects.all().values('created_date_ad', 'created_date_bs', 'qty') \
        .annotate(item_name=F('item__brand_name'),
                  item=F('item'),
                  supplier_customer_name=F('purchase_main__supplier__name'),
                  supplier_customer=F('purchase_main__supplier'),
                  amount=F('amount'),
                  
                  op_type=Case(
                      When(purchase_main__purchase_type=1, then=Value('PURCHASE')),
                      When(purchase_main__purchase_type=2, then=Value('PURCHASE-RETURN')),
                      When(purchase_main__purchase_type=3, then=Value('OPENING-STOCK')),
                      default=Value('N/A'),
                      output_field=models.CharField()))\
        .filter(**filterset) \
        .union(SaleDetail.objects.all().values('created_date_ad', 'created_date_bs', 'qty') \
               .annotate(item_name=F('item__brand_name'),
                         item=F('item'),
                         supplier_customer_name=F('sale_main__customer__first_name'),
                         supplier_customer=F('sale_main__customer'),
                         amount=F('amount'),
                         op_type=Case(
                             When(sale_main__sale_type=1, then=Value('SALE')),
                             When(sale_main__sale_type=2, then=Value('SALE-RETURN')),
                             default=Value('N/A'),
                             output_field=models.CharField(),
                             ),

                         ).filter(**filterset), all=True)

    return query



# """____________________________stock analysis of purchase  opening_______________________________________________________________"""
# 
# 
# def get_remaining_qty_of_purchase_opening(ref_id):
#     stock = get_purchase_qty(ref_id) - get_purchase_return_qty(ref_id) - \
#             get_purchase_sale_qty(ref_id) + get_purchase_sale_return_qty(ref_id)
#     return stock


# # call value id of PurchaseDetail
# def get_purchase_opening_qty(ref_id):
#     total_purchase_qty = sum(PurchaseDetail.objects.filter(pk=ref_id, purchase_main__purchase_type=3)
#                              .values_list('qty', flat=True))
#     return total_purchase_qty


# # call value ref_purchase_detail
# def get_purchase_opening_return_qty(ref_id):
#     total_purchase_return_qty = sum(
#         PurchaseDetail.objects.filter(ref_purchase_detail=ref_id, purchase_main__purchase_type=2)
#             .values_list('qty', flat=True))
#     return total_purchase_return_qty


# # call value ref_purchase_detail
# def get_purchase_opening_sale_qty(ref_id):
#     total_sale_qty = sum(
#         SaleDetail.objects.filter(ref_purchase_detail=ref_id, sale_main__sale_type=1).values_list('qty', flat=True))
#     return total_sale_qty


# # call value ref_purchase_detail
# def get_purchase_opening_sale_return_qty(ref_id):
#     total_sale_return_qty = sum(
#         SaleDetail.objects.filter(ref_purchase_detail=ref_id, sale_main__sale_type=2).values_list('qty', flat=True))
#     return total_sale_return_qty