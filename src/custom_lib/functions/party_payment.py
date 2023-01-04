# queryset operations
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.db.models import F, DecimalField
from django.db import connection
from src.purchase.models import PurchaseMain
from src.supplier.models import Supplier
from django.db.models import Subquery


def get_purchase_credit_detail(supplier=None, purchase_main=None):
    # To calculate Total Credit amount, Paid Amount and Due amount of a bill supplier wise
    if supplier and purchase_main:
        bills = PurchaseMain.objects.filter(pay_type=2, supplier=supplier, id=purchase_main) \
            .order_by('created_date_ad') \
            .values('supplier_id', 'purchase_no') \
            .annotate(
            total_amount=F('total_amount'),
            purchase_id=F('id'),
            created_date_ad=F('created_date_ad'),
            created_date_bs=F('created_date_bs'),
            created_by_user_name=F('created_by__user_name'),
            created_by=F('created_by'),
            remarks=F('remarks'),
            name=F('supplier__name'),
            paid_amount=Coalesce(Sum('partypayment__total_amount'), 0, output_field=DecimalField())
        ) \
            .annotate(due_amount=F('total_amount') - F('paid_amount'))
    elif supplier:
        bills = PurchaseMain.objects.filter(pay_type=2, supplier=supplier) \
            .order_by('created_date_ad') \
            .values('supplier_id', 'purchase_no') \
            .annotate(
            total_amount=F('total_amount'),
            purchase_id=F('id'),
            created_date_ad=F('created_date_ad'),
            created_date_bs=F('created_date_bs'),
            created_by_user_name=F('created_by__user_name'),
            created_by=F('created_by'),
            remarks=F('remarks'),
            name=F('supplier__name'),
            paid_amount=Coalesce(Sum('partypayment__total_amount'), 0, output_field=DecimalField())
        ) \
            .annotate(due_amount=F('total_amount') - F('paid_amount'))
    elif purchase_main:
        bills = PurchaseMain.objects.filter(pay_type=2, id=purchase_main) \
            .order_by('created_date_ad') \
            .values('supplier_id', 'purchase_no') \
            .annotate(
            total_amount=F('total_amount'),
            purchase_id=F('id'),
            created_date_ad=F('created_date_ad'),
            created_date_bs=F('created_date_bs'),
            created_by_user_name=F('created_by__user_name'),
            created_by=F('created_by'),
            remarks=F('remarks'),
            name=F('supplier__name'),
            paid_amount=Coalesce(Sum('partypayment__total_amount'), 0, output_field=DecimalField())
        ) \
            .annotate(due_amount=F('total_amount') - F('paid_amount'))
    else:
        bills = PurchaseMain.objects.filter(pay_type=2) \
            .order_by('created_date_ad') \
            .values('supplier_id', 'purchase_no') \
            .annotate(
            total_amount=F('total_amount'),
            purchase_id=F('id'),
            created_date_ad=F('created_date_ad'),
            date=F('created_date_ad'),
            created_date_bs=F('created_date_bs'),
            created_by_user_name=F('created_by__user_name'),
            created_by=F('created_by'),
            remarks=F('remarks'),
            name=F('supplier__name'),
            paid_amount=Coalesce(Sum('partypayment__total_amount'), 0, output_field=DecimalField())
        ) \
            .annotate(due_amount=F('total_amount') - F('paid_amount'))


    return bills


# def get_supplier_credit_details(supplier=None):
#
#     query = supplier.objects.filter(PurchaseMaster__pay_type=2).values('id')\
#         .annotate(amount=Coalesce(Sum('PurchaseMaster__grand_total'), 0), supplier_name=F('first_name'),
#                   ).annotate(paid_amount=Coalesce(Sum('PurchaseMaster__creditclearancedetail__amount'), 0))
#
#     return query
