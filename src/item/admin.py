'''
urls  register for item app
'''
from django.contrib import admin
from .models import Item,  PoPriority, Strength, Unit,ItemUnit, GenericName,\
    SuperCategory, ProductCategory, MedicineCategory, MedicineForm, GenericStrength
# Register your models here.


class GenericNameAdminModel(admin.ModelAdmin):
    model = GenericName
    ordering = ('id',)
    list_display = ('id', 'name', 'active')

class ItemAdminModel(admin.ModelAdmin):
    model = Item
    search_fields = ('brand_name', )
    list_filter = ('brand_name', )
    ordering = ('id',)
    list_display = ('id', 'brand_name', 'company',  'active')

class PoPriorityAdminModel(admin.ModelAdmin):
    model = PoPriority
    # search_fields = ('brand_name', )
    # list_filter = ('brand_name', )
    # ordering = ('id',)
    list_display = ('id', 'company', 'supplier',  'priority', 'active')

# class GenericStrength(admin.TabularInline):
#     model = GenericStrength

admin.site.register(Unit)
admin.site.register(ItemUnit)
admin.site.register(GenericName, GenericNameAdminModel)
admin.site.register(Item, ItemAdminModel)
admin.site.register(SuperCategory)
admin.site.register(ProductCategory)
admin.site.register(MedicineCategory)
admin.site.register(MedicineForm)
admin.site.register(PoPriority, PoPriorityAdminModel)
admin.site.register(Strength)
admin.site.register(GenericStrength)