from src.core_app.models import CreateInfoModel
from src.item.models import Item, ItemUnit
from django.db import models
from src.custom_lib.functions.field_value_validation import gt_zero_validator
from src.customer.models import Customer
from src.user.models import User

# log import
from log_app.models import LogBase
from simple_history import register

class OrderMain(CreateInfoModel):
    '''
    model for order main
    '''
    DELIVERY_STATUS_TYPE = [
        (1, "PENDING"),
        (2, "CANCELLED"),
        (3, "BILLED"),
        (4, "PACKED"),
        (5, "DISPATCHED"),
        (6, "DONE"),
        (7, "BILLED & PENDING"),
    ]

    AMOUNT_STATUS = [
        (1, "PAID"),
        (2, "UNPAID"),
    ]
    order_no = models.CharField(max_length=20, unique=True, help_text="Order Id should be max. of 13 characters")
    delivery_status = models.PositiveIntegerField(choices=DELIVERY_STATUS_TYPE, default= 1,\
                                        help_text="Where 1 = PENDING, 2 = CANCELLED,  3 = BILLED,  4 = BILLED & PENDING, 5 = PACKED, 6=DISPATCHED, 7=DONE, Default=1")
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name="customer_order")
    delivery_person = models.ForeignKey(User,  on_delete=models.PROTECT, null = True,  blank = True, related_name = "delivery_person", \
                                                help_text= "null = True , blank = True, related name = delivery person")
    amount_status = models.PositiveIntegerField(choices= AMOUNT_STATUS, default = 2,  help_text="Where 1 = PAID, 2 = UNPAID where default = 2")  
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.0, help_text="Total  amount default=0.00")                               
    order_location = models.CharField(max_length=100, help_text=" Order Location should be max. of 100 characters")
    google_location = models.CharField(max_length=100, blank=True, help_text=" Google Location should be max. of 100 characters")
    acknowledge_order = models.BooleanField(default= True, help_text= "Default = True")
    delivery_date_ad = models.DateTimeField(blank=True, null=True, help_text= "blank = True, null = True")
    remarks = models.CharField(max_length=100, blank=True, help_text="Remarks should be max. of 100 characters")

    def __str__(self):
        return "id {}".format(self.id)

register(OrderMain, app="log_app", table_name="customer_order_ordermain_log",
         custom_model_name=lambda x: f'Log{x}',
         use_base_model_db=False, history_user_id_field=models.IntegerField(null=True),
         excluded_fields=['created_date_ad', 'created_date_bs', 'created_by'], bases=[LogBase])


class OrderDetail(CreateInfoModel):
    '''
    model for order detail
    '''
    order = models.ForeignKey(OrderMain, on_delete=models.PROTECT, related_name = 'order_details')
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    qty = models.IntegerField(validators=[gt_zero_validator])
    item_unit = models.ForeignKey(ItemUnit, on_delete=models.PROTECT, blank = True, null = True,\
                                 help_text= "item unit foreign key references from ItemUnit model")
    discount_rate = models.DecimalField(max_digits=12, decimal_places=2, default=0.0,
                    help_text="Discount rate  default 0.00")
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    net_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, help_text='default = 0.00 ')
    sub_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, help_text='default = 0.00 ')
    informed = models.BooleanField(default=False, help_text= "default = false")
    archived = models.BooleanField(default=False, help_text="By default= False")
    cancelled= models.BooleanField(default=False, help_text="By default= False")
    

    def __str__(self):
        return "id {}".format(self.id)


register(OrderDetail, app="log_app", table_name="customer_order_orderdetail_log",
         custom_model_name=lambda x: f'Log{x}',
         use_base_model_db=False, history_user_id_field=models.IntegerField(null=True),
         excluded_fields=['created_date_ad', 'created_date_bs', 'created_by'], bases=[LogBase])


