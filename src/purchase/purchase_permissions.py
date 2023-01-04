from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS

class PurchaseMainPermission(BasePermission):
    
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        if request.user.is_superuser is True:
            return True
        try:
            user_permissions = request.user.group.permissions.values_list('code_name', flat=True)
        except:
            return False
        
        if request.method in SAFE_METHODS and 'view_purchase_main' in user_permissions:
            return True
        
        
        return False

class PurchaseDetailPermission(BasePermission):
    
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        if request.user.is_superuser is True:
            return True
        try:
            user_permissions = request.user.group.permissions.values_list('code_name', flat=True)
        except:
            return False
        
        if request.method in SAFE_METHODS and 'view_purchase_detail' in user_permissions:
            return True
        
        
        return False


class OpeningStockPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        if request.user.is_superuser is True:
            return True
        try:
            user_permissions = request.user.group.permissions.values_list('code_name', flat=True)
        except:
            return False
        if (request.method == 'POST' or request.method in SAFE_METHODS) and 'add_opening_stock' in user_permissions:
            return True
        if request.method in SAFE_METHODS and 'view_opening_stock' in user_permissions:
            return True
        if (request.method == 'PATCH' or request.method in SAFE_METHODS) and 'update_opening_stock' in user_permissions:
            return True
        return False


class PurchaseOrderVerifiedPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        if request.user.is_superuser is True:
            return True
        try:
            user_permissions = request.user.group.permissions.values_list('code_name', flat=True)
        except:
            return False
        if (request.method == 'POST' or request.method in SAFE_METHODS) and 'verify_purchase_order' in user_permissions:
            return True
        return False


class PurchaseReturnPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        if request.user.is_superuser is True:
            return True
        try:
            user_permissions = request.user.group.permissions.values_list('code_name', flat=True)
        except:
            return False
        if (request.method == 'POST' or request.method in SAFE_METHODS) and 'add_purchase_return' in user_permissions:
            return True
        return False



class UpdatePurchaseDetailPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        if request.user.is_superuser is True:
            return True
        try:
            user_permissions = request.user.group.permissions.values_list('code_name', flat=True)
        except:
            return False
      
        if (request.method == 'PATCH' or request.method in SAFE_METHODS) and 'update_purchase_detail' in user_permissions:
            return True
        return False


class DirectPurchasePermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        if request.user.is_superuser is True:
            return True
        try:
            user_permissions = request.user.group.permissions.values_list('code_name', flat=True)
        except:
            return False
        if (request.method == 'POST' or request.method in SAFE_METHODS) and 'direct_purchase' in user_permissions:
            return True
        return False