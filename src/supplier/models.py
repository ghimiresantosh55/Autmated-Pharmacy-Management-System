# Django
from django.db import models
# User-defined models (import)
from src.core_app.models import CreateInfoModel 
# import for log
from log_app.models import LogBase
from simple_history import register


class Supplier(CreateInfoModel ):
    '''
    model for supplier
    '''
    name = models.CharField(max_length=40, help_text="First name can be max. of 40 characters")
    address = models.CharField(max_length=150, help_text="Address can be max. of 150 character")
    phone_no = models.CharField(max_length=30, help_text="Phone no. can be max. of 30 characters")
    pan_vat_no = models.CharField(max_length=10,unique=True, help_text="Pan vat no. can be max. of 10 characters and unique = true")
    latitude = models.CharField(max_length=30, null= True, blank=True, help_text= "Can be blank") 
    longitude = models.CharField(max_length=30,  null= True, blank=True, help_text= "Can be blank")                  
    active = models.BooleanField(default=True, help_text="by default active = True")

    def __str__(self):
        return "id {}".format(self.id, self.name)


register(Supplier, app="log_app", table_name="supplier_supplier_log",
         custom_model_name=lambda x: f'Log{x}',
         use_base_model_db=False, history_user_id_field=models.IntegerField(null=True),
         excluded_fields=['created_date_ad', 'created_date_bs', 'created_by'], bases=[LogBase])


class SupplierContact(CreateInfoModel ):
    '''
    model for supplier contact
    '''
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='supplier_contacts')
    contact_person = models.CharField(max_length=50, help_text="Contact Person  can be max. of 50 characters")
    phone_no = models.CharField(max_length=15, null = True, blank= True, help_text="Phone no. can be max. of 15 characters and blank = True")
    active = models.BooleanField(default=True, help_text="by default active = True")

    def __str__(self):
        return "id {}".format(self.id)


register(SupplierContact, app="log_app", table_name="supplier_supplier_contact_log",
         custom_model_name=lambda x: f'Log{x}',
         use_base_model_db=False, history_user_id_field=models.IntegerField(null=True),
         excluded_fields=['created_date_ad', 'created_date_bs', 'created_by'], bases=[LogBase])
