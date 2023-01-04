from django.db import models
from easy_care import settings
# User-defined models (import)
from src.core_app.models import CreateInfoModel
from typing import Optional, Collection
from django.core.exceptions import ValidationError

from simple_history import register
from log_app.models import LogBase
# Create your models here.


class BloodTestCategory(CreateInfoModel):

    name= models.CharField(max_length=100, unique=True,\
                            help_text=" blood test category name can be max. of 100 characters and must be unique")
    active = models.BooleanField(default=True, help_text="By default active=True")
    def __str__(self):
        return "id {} : {}".format(self.id, self.name)


    def validate_unique(self, exclude: Optional[Collection[str]] = ...) -> None:

      # Custom unique validation check for case insensitive
        if self.id:
           if  BloodTestCategory.objects.exclude(id=self.id).filter(name__iexact=self.name).exists():
             raise ValidationError("This Blood Test Category name already exists")
        else:
           if BloodTestCategory.objects.filter(name__iexact=self.name).exists():
              raise ValidationError("This  Blood Test Category name already exists")
        return super().validate_unique(exclude)

register(BloodTestCategory, app="log_app", table_name="blood_test_category_log", custom_model_name=lambda x: f'Log{x}',
         use_base_model_db=False, history_user_id_field=models.IntegerField(null=True),
         excluded_fields=['created_date_ad', 'created_date_bs', 'created_by','app_type','device_type'], bases=[LogBase])

class BloodTest(CreateInfoModel):

    name =  models.CharField(max_length=100, unique=True,\
                            help_text=" blood test name can be max. of 100 characters and must be unique")

    blood_test_category = models.ManyToManyField(BloodTestCategory, blank=True)
    specimen =  models.CharField(max_length=100, \
                            help_text="specimen can be max. of 100 characters")
    department = models.CharField(max_length=50, \
                            help_text="department can be max. of 50 characters")
    
    method =  models.CharField(max_length=100, \
                            help_text="department can be max. of 100 characters")

    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00,
                                    help_text="Max value  price can be upto 9999999999.99")
    
    reporting= models.CharField(max_length=100, \
                            help_text="department can be max. of 100 characters")
    active = models.BooleanField(default=True, help_text="By default active=True")
    def __str__(self):
        return "id {} : {}".format(self.id, self.name)


    def validate_unique(self, exclude: Optional[Collection[str]] = ...) -> None:

      # Custom unique validation check for case insensitive
        if self.id:
           if  BloodTest.objects.exclude(id=self.id).filter(name__iexact=self.name).exists():
             raise ValidationError("This Blood Test name already exists")
        else:
           if BloodTest.objects.filter(name__iexact=self.name).exists():
              raise ValidationError("This  Blood Test name already exists")
        return super().validate_unique(exclude)

register(BloodTest, app="log_app", table_name="blood_test_log", custom_model_name=lambda x: f'Log{x}',
         use_base_model_db=False, history_user_id_field=models.IntegerField(null=True),
         excluded_fields=['created_date_ad', 'created_date_bs', 'created_by','app_type','device_type'], bases=[LogBase])

class TestPackage(CreateInfoModel):
    name = models.CharField(max_length=100, unique=True,\
                            help_text=" blood test package name can be max. of 100 characters and must be unique")

    test_involved= models.ManyToManyField(BloodTest)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00,
                                    help_text="Max value  price can be upto 9999999999.99")
    active = models.BooleanField(default=True, help_text="By default active=True")

    def __str__(self):
        return "id {} : {}".format(self.id, self.name)


    def validate_unique(self, exclude: Optional[Collection[str]] = ...) -> None:

      # Custom unique validation check for case insensitive
        if self.id:
           if  TestPackage.objects.exclude(id=self.id).filter(name__iexact=self.name).exists():
             raise ValidationError("This Test Package name already exists")
        else:
           if TestPackage.objects.filter(name__iexact=self.name).exists():
              raise ValidationError("This Test package name already exists")
        return super().validate_unique(exclude)

register(TestPackage, app="log_app", table_name="test_package_log", custom_model_name=lambda x: f'Log{x}',
         use_base_model_db=False, history_user_id_field=models.IntegerField(null=True),
         excluded_fields=['created_date_ad', 'created_date_bs', 'created_by','app_type','device_type'], bases=[LogBase])