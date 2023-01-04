from django.utils import timezone
from django.db import models

from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import serializers

# User-defined models (import)
from src.core_app.models import CreateInfoModel
from src.user.models import User
from easy_care import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
# log import
from log_app.models import LogBase
from simple_history import register
from src.custom_lib.functions.date_converter import ad_to_bs_converter
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Customer(models.Model):
    '''
    model for customer
    '''
    user = models.OneToOneField(User, on_delete=models.PROTECT, null=True, blank=True, related_name="customer_user", help_text="Blank= True")
    first_name = models.CharField(max_length=50,  help_text="first Name should be maximum of 50 characters")
    last_name = models.CharField(max_length=50, blank = True,  help_text="last Name should be maximum of 50 characters")
    home_address = models.CharField(max_length=255, help_text="home address should be maximum of 255 characters")
    home_google_location = models.CharField(max_length=255, blank=True, help_text=" home google location should be maximum of 255 characters")
    office_address = models.CharField(max_length=255, blank=True,  help_text=" office address should be maximum of 255 characters")
    office_google_location = models.CharField(max_length=255, blank=True, help_text="office  google location should be maximum of 255 characters")
    phone_no = models.CharField(max_length=15, help_text="Phone no. can be max. of 15 characters")
    client_no =  models.CharField(max_length=15, blank = True, null = True)
    alt_phone_no = models.CharField(max_length=15, blank = True, null = True,  help_text=" Alternative Phone no. can be max. of 15 characters and blank= True")
    created_date_ad = models.DateTimeField(null=True, blank=True)
    created_date_bs = models.CharField(max_length=10, null=True, blank=True, help_text="Blank= True, Null = True")
   
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.created_date_ad = timezone.now()
            date_bs = ad_to_bs_converter(self.created_date_ad)
            self.created_date_bs = date_bs

        super().save(*args, **kwargs)
   
    def __str__(self):
        return self.first_name
  
      
register(Customer, app="log_app", table_name="customer_customer_log",
         custom_model_name=lambda x: f'Log{x}',
         use_base_model_db=False, history_user_id_field=models.IntegerField(null=True),
         excluded_fields=['created_date_ad', 'created_date_bs', 'created_by'], bases=[LogBase])

