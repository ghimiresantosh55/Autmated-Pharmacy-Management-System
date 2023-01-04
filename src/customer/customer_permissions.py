from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS


class CustomerPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        if request.user.is_superuser is True:
            return True
        try:
            user_permissions = request.user.group.permissions.values_list('code_name', flat=True)
        except:
            return False
       
        if request.method in SAFE_METHODS and 'view_customer' in user_permissions:
            return True
        return False


class CustomerUpdatePermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return False
        if request.user.is_superuser is True:
            return True
        permissions_list = request.user.group.permissions.values_list('code_name', flat=True)
        if request.method == 'PATCH' and 'update_customer' in permissions_list:
            return True
        return False