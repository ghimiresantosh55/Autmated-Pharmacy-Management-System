from django.contrib import admin

# Register your models here.
from .models import Company


class CompanyAdminModel(admin.ModelAdmin):
    model = Company
    search_fields = ['name', ]
    ordering = ['id', ]
    list_display = ['id', 'name']
                


admin.site.register(Company, CompanyAdminModel)