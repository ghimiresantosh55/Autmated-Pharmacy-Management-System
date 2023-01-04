'''
model for tenant
'''
from django.db import models

class Tenant(models.Model):
    '''
    model class for tenant
    '''
    name = models.CharField(max_length=100, unique=True)
    schema_name = models.CharField(max_length=100, unique=True)
    sub_domain = models.CharField(max_length=300, unique=True)
    active = models.BooleanField(default=True)
    default= models.BooleanField(default=False, help_text="by default=False")


    def __str__(self):
        return f"{self.name} : {self.sub_domain}"
