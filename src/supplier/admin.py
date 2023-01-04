from django.contrib import admin

# Register your models here.
from .models import Supplier, SupplierContact


class SupplierAdminModel(admin.ModelAdmin):
    model = Supplier
    search_fields = ['name', ]
    ordering = ['id', 'name']
    list_display = ['id', 'name',
                    'phone_no']


admin.site.register(Supplier, SupplierAdminModel)
admin.site.register(SupplierContact)