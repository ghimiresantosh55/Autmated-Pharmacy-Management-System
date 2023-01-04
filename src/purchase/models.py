from django.db import models
#log import
from log_app.models import LogBase
from simple_history import register
from src.purchase_order.models import PurchaseOrderReceivedMain, PurchaseOrderReceivedDetail
from src.core_app.models import CreateInfoModel
from src.item.models import Item, ItemUnit
from django.db import models
from src.custom_lib.functions.field_value_validation import gt_zero_validator
from src.supplier.models import  Supplier
from src.store.models import Location
from django.utils.translation import ugettext_lazy as _

class PurchaseMain(CreateInfoModel):
    '''
    model for purchase main
    '''

    PURCHASE_TYPE = (
        (1, "PURCHASE"),
        (2, "RETURN"),
        (3, "OPENING-STOCK")
        
    )
    PAY_TYPE = (
        (1, "CASH"),
        (2, "CREDIT")
    )
    purchase_no = models.CharField(max_length=20, unique=True, help_text="purchase no  should be max. of 20 characters")
    purchase_type = models.PositiveIntegerField(choices=PURCHASE_TYPE,
                                            help_text="Purchase type like  purchase, return, opening stock")
    pay_type = models.PositiveIntegerField(choices=PAY_TYPE,
                                           help_text="Pay type like 1=CASH, 2=CREDIT")
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, null= True, blank = True, help_text= "null= True, blank = True", related_name = 'purchase_mains')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.0, help_text="Total  amount default=0.00") 
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.0, help_text=" discount amount default=0.00") 
    vat_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.0, help_text=" vat amount default=0.00") 
    bill_no = models.CharField(max_length=20, help_text="Bill no.", blank=True)
    bill_date_ad = models.DateField(max_length=10, help_text="Bill Date AD", blank=True, null=True)
    bill_date_bs = models.CharField(max_length=10, help_text="Bill Date BS", blank=True)
    ref_purchase = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True)
    ref_purchase_order_received_main = models.ForeignKey(PurchaseOrderReceivedMain, on_delete=models.PROTECT, null = True, blank =True, related_name = "purchase_detail")                              
    remarks = models.CharField(max_length=100, blank=True, help_text="Remarks should be max. of 100 characters")

    def __str__(self):
        return "id {}".format(self.id)
    

register(PurchaseMain, app="log_app", table_name="purchase_main_log",
         custom_model_name=lambda x: f'Log{x}',
         use_base_model_db=False, history_user_id_field=models.IntegerField(null=True),
         excluded_fields=['created_date_ad', 'created_date_bs', 'created_by'], bases=[LogBase])




class PurchaseDetail(CreateInfoModel):
    '''
    model for purchase detail
    '''
    purchase_main = models.ForeignKey(PurchaseMain, on_delete=models.PROTECT, related_name = 'purchase_details')
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    qty = models.IntegerField(validators=[gt_zero_validator])
    item_unit = models.ForeignKey(ItemUnit, on_delete=models.PROTECT, blank = True, null = True ,\
                                help_text= "item unit foreign key references from ItemUnit model")
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, help_text='default = 0.00 ')
    discount_rate = models.DecimalField(max_digits=12, decimal_places=2, default=0.0,
                    help_text="Discount rate  default 0.00")
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    net_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    sub_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, help_text='default = 0.00 ')
    ref_purchase_order_received_detail = models.ForeignKey(PurchaseOrderReceivedDetail, on_delete=models.PROTECT, null = True, blank= True)
    ref_purchase_detail = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True)
    location = models.ForeignKey(Location, verbose_name=_("Item location"), null=True, blank=True, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.0,
                                    help_text="Max value  price can be upto 9999999999.99, price means MRP")
    def __str__(self):
        return "id {}".format(self.id)
    
    


register(PurchaseDetail, app="log_app", table_name="purchase_detail_log",
         custom_model_name=lambda x: f'Log{x}',
         use_base_model_db=False, history_user_id_field=models.IntegerField(null=True),
         excluded_fields=['created_date_ad', 'created_date_bs', 'created_by'], bases=[LogBase])



