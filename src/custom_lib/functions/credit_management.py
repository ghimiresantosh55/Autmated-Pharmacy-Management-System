# queryset operations
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.db.models import F, DecimalField
from django.db import connection
from src.sale.models import  SaleMain
from src.customer.models import Customer
from django.db.models import Subquery


def get_sale_credit_detail(customer=None, sale_main=None):
    #To calculate Total Credit amount, Paid Amount and Due amount of a bill customer wise
    if customer and sale_main:
        bills = SaleMain.objects.filter(pay_type=2,sale_type=1, customer=customer, id=sale_main) \
            .order_by('created_date_ad') \
            .values('customer_id', 'sale_no') \
            .annotate(
            total_amount=F('total_amount'),
            sale_id=F('id'),
            created_date_ad=F('created_date_ad'),
            created_date_bs=F('created_date_bs'),
            created_by_user_name=F('created_by__user_name'),
            created_by=F('created_by'),
            remarks=F('remarks'),
            first_name=F('customer__first_name'),
            last_name=F('customer__last_name'),
            paid_amount=Coalesce(Sum('credit_clear__total_amount'), 0, output_field=DecimalField())
        ) \
            .annotate(due_amount=F('total_amount') - F('paid_amount'))
    elif customer:
        bills = SaleMain.objects.filter(pay_type=2,sale_type=1, customer=customer) \
            .order_by('created_date_ad') \
            .values('customer_id', 'sale_no') \
            .annotate(
            total_amount=F('total_amount'),
            sale_id=F('id'),
            created_date_ad=F('created_date_ad'),
            created_date_bs=F('created_date_bs'),
            created_by_user_name=F('created_by__user_name'),
            created_by=F('created_by'),
            remarks=F('remarks'),
            first_name=F('customer__first_name'),
            last_name=F('customer__last_name'),
            paid_amount=Coalesce(Sum('credit_clear__total_amount'), 0, output_field=DecimalField())
        ) \
            .annotate(due_amount=F('total_amount') - F('paid_amount'))
    elif sale_main:
        bills = SaleMain.objects.filter(pay_type=2, sale_type=1, id=sale_main) \
            .order_by('created_date_ad') \
            .values('customer_id', 'sale_no') \
            .annotate(
            total_amount=F('total_amount'),
            sale_id=F('id'),
            created_date_ad=F('created_date_ad'),
            created_date_bs=F('created_date_bs'),
            created_by_user_name=F('created_by__user_name'),
            created_by=F('created_by'),
            remarks=F('remarks'),
            first_name=F('customer__first_name'),
            last_name=F('customer__last_name'),
            paid_amount=Coalesce(Sum('credit_clear__total_amount'), 0, output_field=DecimalField())
        ) \
            .annotate(due_amount=F('grand_total') - F('paid_amount'))
    else:
        bills = SaleMain.objects.filter(pay_type=2) \
            .order_by('created_date_ad') \
            .values('customer_id', 'sale_no') \
            .annotate(
            total_amount=F('total_amount'),
            sale_id=F('id'),
            created_date_ad=F('created_date_ad'),
            date=F('created_date_ad'),
            created_date_bs=F('created_date_bs'),
            created_by_user_name=F('created_by__user_name'),
            created_by=F('created_by'),
            remarks=F('remarks'),
            first_name=F('customer__first_name'),
            last_name=F('customer__last_name'),
            paid_amount=Coalesce(Sum('credit_clear__total_amount'), 0, output_field=DecimalField())
        ) \
            .annotate(due_amount=F('total_amount') - F('paid_amount'))


    return bills


# def get_customer_credit_details(customer=None):
#
#     query = Customer.objects.filter(salemaster__pay_type=2).values('id')\
#         .annotate(amount=Coalesce(Sum('salemaster__grand_total'), 0), customer_name=F('first_name'),
#                   ).annotate(paid_amount=Coalesce(Sum('salemaster__creditclearancedetail__amount'), 0))
#
#     return query
