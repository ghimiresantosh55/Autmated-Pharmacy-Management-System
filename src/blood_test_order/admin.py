from django.contrib import admin
from . models import BloodTestOrderMain

class  BloodTestOrderMainAdminModel(admin.ModelAdmin):
    model =  BloodTestOrderMain
    search_fields = ['id', ]
    ordering = ['-id', ]
    list_display = ['id', 'customer','amount_status','delivery_status']


admin.site.register(BloodTestOrderMain, BloodTestOrderMainAdminModel)

