from django.contrib import admin
from .models import SaleMain, SaleDetail, SalePaymentDetail


class SalePaymentDetailAdmin(admin.ModelAdmin):
     list_display =('id','sale_main','payment_mode','amount','created_date_ad')

# Register your models here.
admin.site.register(SaleMain)
admin.site.register(SaleDetail)
admin.site.register(SalePaymentDetail, SalePaymentDetailAdmin)

