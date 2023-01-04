from django.contrib import admin
from .models import PurchaseMain, PurchaseDetail

# Register your models here.
admin.site.register( PurchaseMain)
admin.site.register( PurchaseDetail)

