from django.db import models
from src.blood_test.models import BloodTest, TestPackage
from src.customer.models import Customer
from src.user.models import User
from src.custom_lib.functions.field_value_validation import gt_zero_validator
# User-defined models (import)
from src.core_app.models import CreateInfoModel
from simple_history import register
from log_app.models import LogBase


class BloodTestOrderMain(CreateInfoModel):

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

    blood_test_order_no = models.CharField(max_length=20, unique=True, help_text=" Blood Test Order Id should be max. of 13 characters")
    delivery_status = models.PositiveIntegerField(choices=DELIVERY_STATUS_TYPE, default= 1,\
                                        help_text="Where 1 = PENDING, 2 = CANCELLED,  3 = BILLED,  4 = BILLED & PENDING, 5 = PACKED, 6=DISPATCHED, 7=DONE, Default=1")
    
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name="blood_test_order")
    delivery_person = models.ForeignKey(User,  on_delete=models.PROTECT, null = True,  blank = True, related_name = "blood_test_delivery_person", \
                                             help_text= "null = True , blank = True, related name = delivery person")
    amount_status = models.PositiveIntegerField(choices= AMOUNT_STATUS, default = 2,  help_text="Where 1 = PAID, 2 = UNPAID where default = 2")                           
    order_location = models.CharField(max_length=100, help_text=" Order Location should be max. of 100 characters")
    google_location = models.CharField(max_length=100, blank=True, help_text=" Google Location should be max. of 100 characters")
    blood_test= models.ManyToManyField(BloodTest)
    test_package= models.ManyToManyField(TestPackage)
    is_blood_test=  models.BooleanField()
    is_test_package= models.BooleanField()
    blood_test= models.ManyToManyField(BloodTest, blank= True)
    test_package= models.ManyToManyField(TestPackage, blank= True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.0, help_text="Total  amount default=0.00")   
    archived = models.BooleanField(default=False, help_text="By default= False")
    remarks = models.CharField(max_length=100, blank=True, help_text="Remarks should be max. of 100 characters")


    def __str__(self):
        return "id {}".format(self.id)

register( BloodTestOrderMain, app="log_app", table_name="blood_test_order_blood_test_order_main_log",
         custom_model_name=lambda x: f'Log{x}',
         use_base_model_db=False, history_user_id_field=models.IntegerField(null=True),
         excluded_fields=['created_date_ad', 'created_date_bs', 'created_by','device_type','app_type'], bases=[LogBase])


