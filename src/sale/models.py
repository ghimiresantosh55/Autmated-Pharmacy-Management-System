from django.db import models

# log import
from log_app.models import LogBase
from simple_history import register
from src.purchase.models import PurchaseMain, PurchaseDetail
from src.customer_order.models import OrderMain, OrderDetail
from src.core_app.models import CreateInfoModel
from src.item.models import Item, ItemUnit
from django.db import models
from src.custom_lib.functions.field_value_validation import gt_zero_validator
from src.customer.models import Customer
from src.core_app.models import PaymentMode


class SaleMain(CreateInfoModel):
    '''
    model for sale main
    '''

    SALE_TYPE = (
        (1, "SALE"),
        (2, "RETURN")

    )
    PAY_TYPE = (
        (1, "CASH"),
        (2, "CREDIT")
    )
    sale_no = models.CharField(max_length=20, unique=True, help_text="Sale No should be max. of 20 characters")
    sale_type = models.PositiveIntegerField(choices=SALE_TYPE,
                                            help_text="Sale type like Sale, Return")

    pay_type = models.PositiveIntegerField(choices=PAY_TYPE, default=1,
                                           help_text="Pay type like 1 = CASH, 2 = CREDIT")
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='sale_mains')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.0,
                                       help_text="Total  amount default=0.00")
    ref_sale_main = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True)
    remarks = models.CharField(max_length=100, blank=True, help_text="Remarks should be max. of 100 characters")
    active = models.BooleanField(default=True, help_text="By default active=True")
    ref_customer_order_main = models.ForeignKey(OrderMain, on_delete=models.PROTECT, blank=True, null=True,
                                                help_text="null = True , blank = True", related_name="sales")

    def __str__(self):
        return "id {}".format(self.id)


register(SaleMain, app="log_app", table_name="sale_main_log",
         custom_model_name=lambda x: f'Log{x}',
         use_base_model_db=False, history_user_id_field=models.IntegerField(null=True),
         excluded_fields=['created_date_ad', 'created_date_bs', 'created_by'], bases=[LogBase])


class SaleDetail(CreateInfoModel):
    '''
    model for  sale detail
    '''
    sale_main = models.ForeignKey(SaleMain, on_delete=models.PROTECT, related_name='sale_details')
    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name="sale_items")
    qty = models.IntegerField(validators=[gt_zero_validator])
    item_unit = models.ForeignKey(ItemUnit, on_delete=models.PROTECT, blank=True, null=True, \
                                  help_text="item unit foreign key references from ItemUnit model")
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, help_text='default = 0.00 ')
    discount_rate = models.DecimalField(max_digits=12, decimal_places=2, default=0.0,
                                        help_text="Discount rate  default 0.00")
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    net_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    sub_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, help_text='default = 0.00 ')
    ref_sale_detail = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True)
    ref_purchase_detail = models.ForeignKey(PurchaseDetail, on_delete=models.PROTECT, null=True, blank=True,
                                            related_name='sales')
    ref_customer_order_detail = models.ForeignKey(OrderDetail, on_delete=models.PROTECT, blank=True, null=True,
                                                  help_text="null = True , blank = True")

    def __str__(self):
        return "id {}".format(self.id)


register(SaleDetail, app="log_app", table_name="sale_detail_log",
         custom_model_name=lambda x: f'Log{x}',
         use_base_model_db=False, history_user_id_field=models.IntegerField(null=True),
         excluded_fields=['created_date_ad', 'created_date_bs', 'created_by'], bases=[LogBase])


class SalePaymentDetail(CreateInfoModel):
    '''
    model for  sale payment detail
    '''
    sale_main = models.ForeignKey(SaleMain, on_delete=models.PROTECT, related_name="payment_details")
    payment_mode = models.ForeignKey(PaymentMode, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=12, decimal_places=2,
                                 help_text="Amount can have max value upto=9999999999.99 and min_value=0.0")
    remarks = models.CharField(max_length=50, blank=True,
                               help_text="Remarks can have max upto 50 characters and blank=True")

    def __str__(self):
        return "id {} : sale {}".format(self.id, self.sale_main)


register(SalePaymentDetail, app="log_app", table_name="sale_salepaymentdetail_log",
         custom_model_name=lambda x: f'Log{x}',
         use_base_model_db=False, history_user_id_field=models.IntegerField(null=True),
         excluded_fields=['created_date_ad', 'created_date_bs', 'created_by'], bases=[LogBase])
