'''
model for care app
'''
# Django libaries
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from typing import Optional, Collection

# custom functions import
from src.custom_lib.functions.date_converter import ad_to_bs_converter
User = get_user_model()
# log import
from log_app.models import LogBase
from simple_history import register

# User-defined models
def upload_path_organization(instance, filename):
    return '/'.join(['organization', filename])

def upload_path_flag_image(instance, filename):
    return '/'.join(['country_flag', filename])


def validate_image(image):
    '''
    Function for validate Image Size
    '''
    file_size = image.size
    limit_byte_size = settings.MAX_UPLOAD_SIZE
    if file_size > limit_byte_size:
        # converting into kb
        f = limit_byte_size / 1024
        # converting into MB
        f = f / 1024
        raise ValidationError("Max size of file is %s MB" % f)


class CreateInfoModel(models.Model):
    '''
    Parent model for created date ad, created date bs and created by and device type, app type
    '''
    DEVICE_TYPE = [
        (1,"Mobile"),
        (2,"PC"),
        (3,"Tablet"),
        (4,"Other"),
        (5,"NA")
    ]
    APP_TYPE =[
        (1,'Web-App'),
        (2, 'IOS-App'),
        (3, 'Android-App'),
        (4,"NA")

    ]
    
    created_date_ad = models.DateTimeField()
    created_date_bs = models.CharField(max_length=10)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    device_type = models.PositiveBigIntegerField(choices=DEVICE_TYPE, default=5, help_text="where 1=Mobile, 2=PC, 3=Tablet and 4=Other")
    app_type  = models.PositiveBigIntegerField(choices=APP_TYPE, default= 4, help_text="where 1=Web-App, 2=IOS-APP, 3=Android-APP")

    def save(self, *args, **kwargs):
        '''
        This method will convert ad date to bs date
        '''
        date_bs = ad_to_bs_converter(self.created_date_ad)
        self.created_date_bs = date_bs
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class OrganizationSetup(CreateInfoModel):
    '''
    model for organization setup
    '''
    '''
    CreateInfoModel model is Inheritance model to get created date ad, bs and created by in this model
    '''
    name = models.CharField(max_length=100, unique=True,
                            help_text="Organization name should be maximum of 100 characters")
    address = models.CharField(max_length=100, unique=True, blank=True,
                               help_text="Organization name should be maximum of 100 characters")
   
    phone_no_1 = models.CharField(max_length=15, unique=True, blank=True,
                                  help_text="Phone no should be maximum of 15 characters")
    phone_no_2 = models.CharField(max_length=15, blank=True, help_text="Phone no should be maximum of 15 characters")
    mobile_no = models.CharField(max_length=15, unique=True, blank=True,
                                 help_text="Mobile no should be maximum of 15 characters")
    pan_no = models.CharField(max_length=15, unique=True, blank=True,
                              help_text="PAN no. should be maximum of 15 characters")
    owner_name = models.CharField(max_length=50, unique=True, blank=True,
                                  help_text="Owner name should be maximum of 50 characters")
    email = models.CharField(max_length=70, unique=True, blank=True,
                             help_text="Email Id. should be maximum of 70 characters")
    website_url = models.CharField(max_length=50, unique=True, blank=True,
                                   help_text="Website address should be maximum of 50 characters")
    logo = models.ImageField(upload_to="organization_setup/logo", validators=[validate_image], blank=True, help_text="")
    favicon = models.ImageField(upload_to="organization_setup/favicon", validators=[validate_image], blank=True,
                                help_text="")

    def __str__(self):
        return "id {} : {}".format(self.id, self.name)


    def validate_unique(self, exclude: Optional[Collection[str]] = ...) -> None:

      # Custom unique validation check for case insensitive
        if self.id:
           if OrganizationSetup.objects.exclude(id=self.id).filter(name__iexact=self.name).exists():
             raise ValidationError("this Organization name already exists")

        if OrganizationSetup.objects.exclude(id=self.id).filter(address__iexact=self.address).exists():
             raise ValidationError("this Organization address already exists")

        if OrganizationSetup.objects.exclude(id=self.id).filter(email__iexact=self.email).exists():
             raise ValidationError("this Organization email already exists")

        if OrganizationSetup.objects.exclude(id=self.id).filter(phone_no_1__iexact=self.phone_no_1).exists():
             raise ValidationError("this Organization phone no 1 already exists")

        if OrganizationSetup.objects.exclude(id=self.id).filter(pan_no__iexact=self.pan_no).exists():
             raise ValidationError("this Organization pan no already exists")

        if OrganizationSetup.objects.exclude(id=self.id).filter(owner_name__iexact=self.owner_name).exists():
             raise ValidationError("this Organization owner  name already exists")

        else:
           if OrganizationSetup.objects.filter(name__iexact=self.name).exists():
              raise ValidationError("this Organization name already exists")

           if OrganizationSetup.objects.filter(address__iexact=self.address).exists():
              raise ValidationError("this Organization address already exists")

           if OrganizationSetup.objects.filter(email__iexact=self.email).exists():
              raise ValidationError("this Organization email already exists")

           if OrganizationSetup.objects.filter(phone_no_1__iexact=self.phone_no_1).exists():
              raise ValidationError("this Organization phone no 1 already exists")

           if OrganizationSetup.objects.filter(pan_no__iexact=self.pan_no).exists():
              raise ValidationError("this Organization pan no already exists")

           if OrganizationSetup.objects.filter(owner_name__iexact=self.owner_name).exists():
              raise ValidationError("this Organization owner name already exists")

        return super().validate_unique(exclude)
        

register(OrganizationSetup, app="log_app", table_name="core_app_organizationsetup_log", custom_model_name=lambda x: f'Log{x}',
         use_base_model_db=False, history_user_id_field=models.IntegerField(null=True),
         excluded_fields=['created_date_ad', 'created_date_bs', 'created_by'], bases=[LogBase])


class OrganizationRule(CreateInfoModel):
    '''
    model for organization rule
    '''
    '''
    CreateInfoModel model is Inheritance model to get created date ad, bs and created by in this model
    '''
    CUSTOMER_SEQUENCE_TYPE = [
        (1,"AD"),
        (2,"BS"),
        (3,"SEQUENTIAL")
    ]

    CALENDAR_SYSTEM = [
        (1, "AD"),
        (2, "BS")
    ]

    DAYS_OF_WEEK = [
        (1, "SUNDAY"),
        (2, "MONDAY"),
        (3, "TUESDAY"),
        (4, "WEDNESDAY"),
        (5, "THURSDAY"),
        (6, "FRIDAY"),
        (7, "SATURDAY"),
    ]

    TAX_SYSTEM = [
        (1, "VAT"),
        (2, "PAN")
    ]
    customer_seq_type = models.PositiveIntegerField(choices=CUSTOMER_SEQUENCE_TYPE, default= 2,\
                                    help_text="where 1=AD,2=BS,3=SEQUENTIAL  and default=2")
    fiscal_session_type = models.PositiveIntegerField(choices=CALENDAR_SYSTEM, default=2,\
                                    help_text="Where 1 = AD , 2 = BS and default=2")
    calendar_system = models.PositiveIntegerField(choices=CALENDAR_SYSTEM, default=2,\
                                    help_text="Where 1 = AD , 2 = BS and default=2")
    enable_print = models.BooleanField(default=True)
    print_preview = models.BooleanField(default=True)
    billing_time_restriction = models.BooleanField(default=False)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    first_day_of_week = models.PositiveIntegerField(choices=DAYS_OF_WEEK, default=1,
                                                    help_text="where 1 = Sunday ---- 7 =Saturday")
    tax_system = models.PositiveIntegerField(choices=TAX_SYSTEM, default=1, help_text="where 1=VAT, 2=PAN")
    round_off_limit = models.PositiveIntegerField(default=2)
    round_off_purchase = models.BooleanField(default=True)
    round_off_sale = models.BooleanField(default=True)
    item_expiry_date_sale_threshold = models.PositiveIntegerField(default=30)
    tax_applicable = models.BooleanField(default=True)
    tax_rate = models.FloatField(default=0.0, validators=[MinValueValidator(0), MaxValueValidator(100)],
                                 help_text="Tax rate")

    def __str__(self):
        return "id {} : {}".format(self.id, self.get_calendar_system_display())

register(OrganizationRule, app="log_app", table_name="core_app_organizationrule_log",
         custom_model_name=lambda x: f'Log{x}',
         use_base_model_db=False, history_user_id_field=models.IntegerField(null=True),
         excluded_fields=['created_date_ad', 'created_date_bs', 'created_by'], bases=[LogBase])


class AppAccessLog(CreateInfoModel):
    '''
    model for app access log
    '''
    '''
    CreateInfoModel model is Inheritance model to get created date ad, bs and created by in this model
    '''
    DEVICE_TYPE = [
        (1,"Mobile"),
        (2,"PC"),
        (3,"Tablet"),
        (4,"Other"),
        (5,"NA")
        
    ]
    APP_TYPE =[
        (1,'Web-App'),
        (2, 'IOS-App'),
        (3, 'Android-App'),
        (4,"NA")

    ]
    device_type = models.PositiveBigIntegerField(choices=DEVICE_TYPE, default=5, help_text="where 1=Mobile, 2=PC, 3=Tablet and 4=Other")
    app_type  = models.PositiveBigIntegerField(choices=APP_TYPE, default=4, help_text="where 1=Web-App, 2=IOS-APP, 3=Android-APP")

    def __str__(self):
        return f'{self.id}'

register(AppAccessLog, app="log_app", table_name="core_app_appaccesslog_log",
         custom_model_name=lambda x: f'Log{x}',
         use_base_model_db=False, history_user_id_field=models.IntegerField(null=True),
         excluded_fields=['created_date_ad', 'created_date_bs', 'created_by'], bases=[LogBase])



class PaymentMode(CreateInfoModel):
    '''
    model for payment mode
    '''
    '''
    CreateInfoModel model is Inheritance model to get created date ad, bs and created by in this model
    '''
    name = models.CharField(max_length=15, unique=True)
    active = models.BooleanField(default=0)
    remarks = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.name}"


register(PaymentMode, app="log_app", table_name="core_app_paymentmode_log",
         custom_model_name=lambda x: f'Log{x}',
         use_base_model_db=False, history_user_id_field=models.IntegerField(null=True),
         excluded_fields=['created_date_ad', 'created_date_bs', 'created_by'], bases=[LogBase])