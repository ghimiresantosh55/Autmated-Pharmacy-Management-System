from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


class UserAdminConfig(UserAdmin):
    model = User
    search_fields = ('email', 'user_name',)
    list_filter = ('email', 'user_name', 'first_name', 'active', 'is_staff')
    ordering = ('-created_date_ad',)
    list_display = ('user_name', 'email', 'active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'user_name', 'password', 'gender','user_type' ,'birth_date', 'group', 'photo', 'created_date_ad',
                           'created_date_bs')}),
        ('Permissions', {'fields': ('is_staff', 'active', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'password1', 'password2', 'group', 'user_type' ,'active', 'created_date_ad',
                       'created_date_bs', 'is_staff', 'gender', 'birth_date', 'created_by', 'photo')}
         ),
    )


admin.site.register(User, UserAdminConfig)
