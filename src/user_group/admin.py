from django.contrib import admin
from .models import UserGroup, UserPermission, UserPermissionCategory
from django.contrib.auth.models import Group
from django.shortcuts import render
from django import forms
from django.urls import path
from django.db import connection, connections


class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()

class PermissionCategoryAdmin(admin.ModelAdmin):
    model = UserPermissionCategory
    search_fields = ('name',)
    list_display = ('id', 'name', 'created_date_ad',  'created_date_bs', 'created_by')
    


    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/',self.upload_csv),]
        return new_urls + urls


    def upload_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES['csv_upload']
            file_data = csv_file.read().decode("utf-8")
            csv_data = file_data.split("\n")
            print(len(csv_data))
            # print("data of csv")
            with connection.cursor() as cursor:
                for data in csv_data:
                    # print('data: ', data)
                    fields = data.split(",")
                    connections['default'].cursor().execute(f"SET search_path to customer1")
                    cursor.execute(f'''insert into branch_ktm.user_group_userpermissioncategory values( {fields[0]}, '{fields[1]}', '{fields[2]}' , '{fields[3]}', {fields[4]} );''')

        form = CsvImportForm()
        data = {"form":form}
        return render(request,"admin/user_group/userpermissioncategory/csv_upload.html", data)


class PermissionAdmin(admin.ModelAdmin):
    model = UserPermission
    search_fields = ('code_name',)
    list_display = ('id', 'name','code_name', 'category','created_date_ad',  'created_date_bs', 'created_by')
    

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/',self.upload_csv),]
        return new_urls + urls

    def upload_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES['csv_upload']
            file_data = csv_file.read().decode("utf-8")
            csv_data = file_data.split("\n")
            print(len(csv_data))
            # print("data of csv")
            with connection.cursor() as cursor:
                for data in csv_data:
                    # print('data: ', data)
                    fields = data.split(",")
                    connections['default'].cursor().execute(f"SET search_path to customer1")
                    cursor.execute(f'''insert into branch_ktm.user_group_userpermission values( {fields[0]}, '{fields[1]}', '{fields[2]}' , '{fields[3]}', '{fields[4]}', {fields[5]}, {fields[6]});''')

        form = CsvImportForm()
        data = {"form":form}
        return render(request,"admin/user_group/userpermission/csv_upload.html", data)

admin.site.unregister(Group)
admin.site.register(UserGroup)
admin.site.register(UserPermission,  PermissionAdmin)
admin.site.register(UserPermissionCategory, PermissionCategoryAdmin)