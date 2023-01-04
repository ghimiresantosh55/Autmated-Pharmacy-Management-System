from django.contrib import admin
from .models import PurchaseOrderMain, PurchaseOrderDetail, PurchaseOrderReceivedMain, PurchaseOrderReceivedDetail



class PurchaseOrderDetailAdminConfig(admin.ModelAdmin):
    model = PurchaseOrderDetail
    list_display = ('id', 'available', 'purchase_order_main', 'item', 'qty', 'net_amount')
    # list_filter = ('item', 'purchase_order_main',)
class InlinePurchaseOrderDetails(admin.TabularInline):
    model = PurchaseOrderDetail

class OrderMainAdminConfig(admin.ModelAdmin):
    model = PurchaseOrderMain
    inlines =[InlinePurchaseOrderDetails] 
    list_display = ('id', 'purchase_order_type',  'total_amount', 'supplier')
    # list_filter = ('supplier', )

# Register your models here.
admin.site.register( PurchaseOrderMain, OrderMainAdminConfig)
admin.site.register( PurchaseOrderDetail, PurchaseOrderDetailAdminConfig)
admin.site.register( PurchaseOrderReceivedMain)
admin.site.register( PurchaseOrderReceivedDetail)

