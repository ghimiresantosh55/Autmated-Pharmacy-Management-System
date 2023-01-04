from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS

class SaleDetailPermission(BasePermission):
    ''''
    custom permission for  sale detail
    '''
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        if request.user.is_superuser is True:
            return True
        try:
            user_permissions = request.user.group.permissions.values_list('code_name', flat=True)
        except:
            return False
       
        if request.method in SAFE_METHODS and 'view_sale_detail' in user_permissions:
            return True
        
        return False



class SaveSalePermission(BasePermission):
    ''''
    custom permission for  save sale
    '''
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        if request.user.is_superuser is True:
            return True
        try:
            user_permissions = request.user.group.permissions.values_list('code_name', flat=True)
        except:
            return False
        if (request.method == 'POST' or request.method in SAFE_METHODS) and 'add_save_sale' in user_permissions:
            return True
        if request.method in SAFE_METHODS and 'view_save_sale' in user_permissions:
            return True
        if (request.method == 'PATCH' or request.method in SAFE_METHODS) and 'update_save_sale' in user_permissions:
            return True
        return False


class SaleMainPermission(BasePermission):
    ''''
    custom permission for sale main
    '''
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        if request.user.is_superuser is True:
            return True
        try:
            user_permissions = request.user.group.permissions.values_list('code_name', flat=True)
        except:
            return False
       
        if request.method in SAFE_METHODS and 'view_sale_main' in user_permissions:
            return True
        
        return False



class SaleReturnPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        if request.user.is_superuser is True:
            return True
        try:
            user_permissions = request.user.group.permissions.values_list('code_name', flat=True)
        except:
            return False
        if (request.method == 'POST' or request.method in SAFE_METHODS) and 'add_sale_return' in user_permissions:
            return True
        return False


class SaleViewPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        if request.user.is_superuser is True:
            return True
        try:
            user_permissions = request.user.group.permissions.values_list('code_name', flat=True)
        except:
            return False
        if request.method in SAFE_METHODS and ('view_sale' in user_permissions or 'add_sale' in user_permissions or
                                               'add_sale_return' in user_permissions):
            return True
        return False

