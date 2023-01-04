from django.contrib import admin
from .models import OrderMain, OrderDetail


class OrderDetailAdminConfig(admin.ModelAdmin):
    model = OrderDetail
    list_display = ('id', 'order', 'item', 'qty', 'informed', 'net_amount', 'archived')

class InlineOrderDetails(admin.TabularInline):
    model = OrderDetail

class OrderMainAdminConfig(admin.ModelAdmin):
    model = OrderMain
    inlines =[InlineOrderDetails] 
    list_display = ('id', 'delivery_status','delivery_person','acknowledge_order','amount_status','total_amount')
 


# Register your models here.
admin.site.register(OrderDetail, OrderDetailAdminConfig)
admin.site.register(OrderMain, OrderMainAdminConfig)

