
from pickle import TRUE
import re
from src.core_app.models import CreateInfoModel
from src.item.models import Item, ItemUnit
from django.db import models
from src.custom_lib.functions.field_value_validation import gt_zero_validator
from src.supplier.models import  Supplier
from src.user.models import User

#log import
from log_app.models import LogBase
from simple_history import register

class PurchaseOrderMain(CreateInfoModel):
    '''
    model for purchase order main
    '''

    PURCHASE_ORDER_TYPE = (
        (1, "ORDER"),
        (2, "CANCELLED"),
        (3, "RECEIVED")
    )
    purchase_order_type = models.PositiveIntegerField(choices=PURCHASE_ORDER_TYPE,
                                            help_text="Order type like Order, approved, cancelled")
    assigned_to = models.ForeignKey(User, on_delete=models.PROTECT, null = TRUE, blank = True, related_name= 'PurchaseOrderMain_assigned_to')
    purchase_order_no = models.CharField(max_length=20, unique=True, help_text="Order Id should be max. of 13 characters")
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.0, help_text="Total  amount default=0.00") 
    search_list = models.BooleanField(default= False, help_text="by default false")                              
    remarks = models.CharField(max_length=100, blank=True, help_text="Remarks should be max. of 100 characters")
    ref_purchase_order_main = models.OneToOneField('self', on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return "id {}".format(self.id)

register(PurchaseOrderMain, app="log_app", table_name="purchase_order_ordermain_log",
         custom_model_name=lambda x: f'Log{x}',
         use_base_model_db=False, history_user_id_field=models.IntegerField(null=True),
         excluded_fields=['created_date_ad', 'created_date_bs', 'created_by'], bases=[LogBase])


class PurchaseOrderDetail(CreateInfoModel):
    '''
    model for purchase order detail
    '''
    AVAILABLE= (
        (1, "PENDING"),
        (2, "RECEIVED"),
        (3, "VERIFIED"),
        (4, "CANCELLED")
    )
   
    available = models.PositiveIntegerField(choices=AVAILABLE, default=1, 
                                            help_text="available like pending, approved, purchased, default = 1")
    purchase_order_main = models.ForeignKey(PurchaseOrderMain, on_delete=models.PROTECT, related_name = 'purchase_order_details')
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
    ref_purchase_order_detail = models.ForeignKey('self', on_delete=models.PROTECT, blank=True,
                                                  null=True)

    def __str__(self):
        return "id {}".format(self.id)


register(PurchaseOrderDetail, app="log_app", table_name="purchase_order_orderdetail_log",
         custom_model_name=lambda x: f'Log{x}',
         use_base_model_db=False, history_user_id_field=models.IntegerField(null=True),
         excluded_fields=['created_date_ad', 'created_date_bs', 'created_by'], bases=[LogBase])




class PurchaseOrderReceivedMain(CreateInfoModel):
    '''
    model for purchase order received main
    '''
    
    PURCHASE_ORDER_RECEIVED_TYPE = (
        (1, "UNVERIFIED"),
        (2, "VERIFIED")
      
    )
    purchase_order_received_type = models.PositiveIntegerField(choices=PURCHASE_ORDER_RECEIVED_TYPE,
                                            help_text="1 =unverified, 2 = verified")
    purchase_order_received_no = models.CharField(max_length=20, unique=True, help_text="receive no  should be max. of  20 characters")
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.0, help_text="Total  amount default=0.00")                           
    remarks = models.CharField(max_length=100, blank=True, help_text="Remarks should be max. of 100 characters")
    purchase_order_main = models.ForeignKey(PurchaseOrderMain, on_delete=models.PROTECT, blank=True, null=True)
    ref_purchase_order_received_main = models.OneToOneField('self', on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return "id {}".format(self.id)

register(PurchaseOrderReceivedMain, app="log_app", table_name="purchase_order_purchaseorderreceivedmain_log",
         custom_model_name=lambda x: f'Log{x}',
         use_base_model_db=False, history_user_id_field=models.IntegerField(null=True),
         excluded_fields=['created_date_ad', 'created_date_bs', 'created_by'], bases=[LogBase])



class PurchaseOrderReceivedDetail(CreateInfoModel):
    '''
    model for purchase order received detail
    '''
    purchase_order_received_main = models.ForeignKey(PurchaseOrderReceivedMain, on_delete=models.PROTECT, related_name = 'purchase_order_received_details')
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    qty = models.IntegerField(validators=[gt_zero_validator])
    item_unit = models.ForeignKey(ItemUnit, on_delete=models.PROTECT, blank = True, null = True,\
                             help_text= "item unit foreign key references from ItemUnit model")
    discount_rate = models.DecimalField(max_digits=12, decimal_places=2, default=0.0,
                    help_text="Discount rate  default 0.00")
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    net_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, help_text='default = 0.00 , amount means cost of item')
    sub_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, help_text='default =0.00 , sub_total means amount(cost)*qty ')
    purchase_order_detail = models.ForeignKey(PurchaseOrderDetail, on_delete=models.PROTECT, blank=True,
                                                  null=True)
    ref_purchase_order_received_detail = models.ForeignKey('self', on_delete=models.PROTECT, blank=True,
                                                  null=True)

    archived = models.BooleanField(default=False, help_text="By default= False")
    def __str__(self):
        return "id {}".format(self.id)


register(PurchaseOrderReceivedDetail, app="log_app", table_name="purchase_order_purchaseorderreceiveddetail_log",
         custom_model_name=lambda x: f'Log{x}',
         use_base_model_db=False, history_user_id_field=models.IntegerField(null=True),
         excluded_fields=['created_date_ad', 'created_date_bs', 'created_by'], bases=[LogBase])