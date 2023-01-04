'''
admin site register for core app
'''
from ctypes.wintypes import PBOOLEAN
from django.contrib import admin
from .models import OrganizationRule, OrganizationSetup
from .models import  AppAccessLog, PaymentMode
# Register your models here.
# Register your models here.

admin.site.register(OrganizationRule)
admin.site.register(OrganizationSetup)
admin.site.register(AppAccessLog)
admin.site.register(PaymentMode)

