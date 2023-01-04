
from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS


class PublicUserChangePasswordPermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return False
        if request.user.is_superuser is True:
            return True
        permissions_list = request.user.group.permissions.values_list('code_name', flat=True)
        if request.method == 'PATCH' and 'change_user_password' in permissions_list:
            return True
        elif request.user.id == obj.id:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or (obj and obj.id == request.user.id)

class PublicUserViewPermissions(BasePermission):


    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False

        if request.user.is_superuser is True:
            return True
        try:
            user_permissions = request.user.group.permissions.values_list('code_name', flat=True)
        except:
            return False

        if request.method in SAFE_METHODS and 'view_public_user' in user_permissions:
            return True
        
        return False


    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or (obj and obj.id == request.user.id)



class PublicUserRetrievePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return False
        if request.user.is_superuser is True:
            return True
        if request.user.id == obj.id:
            return True
        return False


class AddToCartPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        if request.user.is_superuser is True:
            return True
        try:
            user_permissions = request.user.group.permissions.values_list('code_name', flat=True)
        except:
            return False
        if (request.method == 'POST' or request.method in SAFE_METHODS) and 'can_add_cart' in user_permissions:
            return True
        return False