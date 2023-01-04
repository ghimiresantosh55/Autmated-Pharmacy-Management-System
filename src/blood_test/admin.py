from django.contrib import admin
from . models import BloodTest, BloodTestCategory,TestPackage
# Register your models here.

class BloodTestCategoryAdminModel(admin.ModelAdmin):
    model = BloodTestCategory
    search_fields = ['name', ]
    ordering = ['id', ]
    list_display = ['id', 'name']


class BloodTestAdminModel(admin.ModelAdmin):
    model = BloodTest
    search_fields = ['name', ]
    ordering = ['id', ]
    list_display = ['id', 'name']


class TestPackageAdminModel(admin.ModelAdmin):
    model = TestPackage
    search_fields = ['name', ]
    ordering = ['id', ]
    list_display = ['id', 'name']


admin.site.register(BloodTestCategory, BloodTestCategoryAdminModel)
admin.site.register(BloodTest, BloodTestAdminModel)
admin.site.register(TestPackage, TestPackageAdminModel)
                
