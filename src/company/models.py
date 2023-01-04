'''
model for company app
'''
# Django
from django.db import models
# User-defined models (import)
from src.core_app.models import CreateInfoModel
from easy_care import settings
# import for log
from log_app.models import LogBase
from simple_history import register
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


def validate_image(image):
    '''
    Function for validate image size for upload
    '''
    file_size = image.size
    limit_byte_size = settings.MAX_UPLOAD_SIZE
    if file_size > limit_byte_size:
        # converting into kb
        f = limit_byte_size / 1024
        # converting into MB
        f = f / 1024
        raise ValidationError("Max size of file is %s MB" % f)

class Company(CreateInfoModel):
    '''
    model for company
    '''
    name = models.CharField(max_length= 150, help_text="name can be max. of 150 characters")
    feature_brand = models.BooleanField(default=True, help_text="by default active = True")
    phone_no = models.CharField(max_length=15, blank = True, null = True, help_text="Phone no. can be max. of 15 characters and blank = True, null = True")
    address = models.CharField(max_length=50, blank=True, help_text="Address can be max. of 50 characters and blank = True")
    brand_image = models.ImageField(upload_to="brand_image", validators=[validate_image], blank=True, help_text= "blank  true")
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.0,
                                   help_text= "default=0.0 and can be upto 100.00")
    purchase_cc_rate = models.DecimalField(default=0.0, decimal_places=2, max_digits=4, validators=[MinValueValidator(0), MaxValueValidator(100)])
    active = models.BooleanField(default=True, help_text="by default active = True")

    def __str__(self):
        return "id {}".format(self.id, self.name)


register(Company, app="log_app", table_name="compay_company_log",
         custom_model_name=lambda x: f'Log{x}',
         use_base_model_db=False, history_user_id_field=models.IntegerField(null=True),
         excluded_fields=['created_date_ad', 'created_date_bs', 'created_by'], bases=[LogBase])
