from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS


class UnitPermission(BasePermission):
    '''
    custom permission for unit
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
        if request.method in SAFE_METHODS and 'view_unit' in user_permissions:
            return True
        if (request.method == 'POST' or request.method in SAFE_METHODS) and 'add_unit' in user_permissions:
            return True
        if (request.method == 'PATCH' or request.method in SAFE_METHODS) and 'update_unit' in user_permissions:
            return True
        return False



class ItemUnitPermission(BasePermission):
    '''
    custom permission for unit
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
        if request.method in SAFE_METHODS and 'view_item_unit' in user_permissions:
            return True
        if (request.method == 'POST' or request.method in SAFE_METHODS) and 'add_item_unit' in user_permissions:
            return True
        if (request.method == 'PATCH' or request.method in SAFE_METHODS) and 'update_item_unit' in user_permissions:
            return True
        return False


class GenericNamePermission(BasePermission):
    '''
    custom permission for generic name
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
        if request.method in SAFE_METHODS and 'view_generic_name' in user_permissions:
            return True
        if (request.method == 'POST' or request.method in SAFE_METHODS) and 'add_generic_name' in user_permissions:
            return True
        if (request.method == 'PATCH' or request.method in SAFE_METHODS) and 'update_generic_name' in user_permissions:
            return True
        return False


class ItemPermission(BasePermission):
    '''
    custom permission for item
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
        if (request.method == 'POST' or request.method in SAFE_METHODS) and 'add_item' in user_permissions:
            return True
        if request.method in SAFE_METHODS and 'view_item' in user_permissions:
            return True
        if (request.method == 'PATCH' or request.method in SAFE_METHODS) and 'update_item' in user_permissions:
            return True
        return False



class SuperCategoryPermission(BasePermission):
    '''
    custom permission for super category
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
        if (request.method == 'POST' or request.method in SAFE_METHODS) and 'add_super_category' in user_permissions:
            return True
        if request.method in SAFE_METHODS and 'view_super_category' in user_permissions:
            return True
        if (request.method == 'PATCH' or request.method in SAFE_METHODS) and 'update_super_category' in user_permissions:
            return True
        return False


class ProductCategoryPermission(BasePermission):
    '''
    custom permission for product category
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
        if (request.method == 'POST' or request.method in SAFE_METHODS) and 'add_product_category' in user_permissions:
            return True
        if request.method in SAFE_METHODS and 'view_product_category' in user_permissions:
            return True
        if (request.method == 'PATCH' or request.method in SAFE_METHODS) and 'update_product_category' in user_permissions:
            return True
        return False


class MedicineCategoryPermission(BasePermission):
    '''
    custom permission for medicine category
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
        if (request.method == 'POST' or request.method in SAFE_METHODS) and 'add_medicine_category' in user_permissions:
            return True
        if request.method in SAFE_METHODS and 'view_medicine_category' in user_permissions:
            return True
        if (request.method == 'PATCH' or request.method in SAFE_METHODS) and 'update_medicine_category' in user_permissions:
            return True
        return False



class MedicineFormPermission(BasePermission):
    ''''
    custom permission for  medicine form
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
        if (request.method == 'POST' or request.method in SAFE_METHODS) and 'add_medicine_form' in user_permissions:
            return True
        if request.method in SAFE_METHODS and 'view_medicine_form' in user_permissions:
            return True
        if (request.method == 'PATCH' or request.method in SAFE_METHODS) and 'update_medicine_form' in user_permissions:
            return True
        return False


class PoPriorityPermission(BasePermission):
    ''''
    custom permission for  medicine form
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
        if (request.method == 'POST' or request.method in SAFE_METHODS) and 'add_po_priority' in user_permissions:
            return True
        if request.method in SAFE_METHODS and 'view_po_priority' in user_permissions:
            return True
        if (request.method == 'PATCH' or request.method in SAFE_METHODS) and 'update_po_priority' in user_permissions:
            return True
        return False


class StrengthPermission(BasePermission):
    ''''
    custom permission for  medicine form
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
        if (request.method == 'POST' or request.method in SAFE_METHODS) and 'add_strength' in user_permissions:
            return True
        if request.method in SAFE_METHODS and 'view_strength' in user_permissions:
            return True
        if (request.method == 'PATCH' or request.method in SAFE_METHODS) and 'update_strength' in user_permissions:
            return True
        return False



class GenericStrengthPermission(BasePermission):
    
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        if request.user.is_superuser is True:
            return True
        try:
            user_permissions = request.user.group.permissions.values_list('code_name', flat=True)
        except:
            return False
        if (request.method == 'POST' or request.method in SAFE_METHODS) and 'add_generic_strength' in user_permissions:
            return True
        if request.method in SAFE_METHODS and 'view_generic_strength' in user_permissions:
            return True
        if (request.method == 'PATCH' or request.method in SAFE_METHODS) and 'update_generic_strength' in user_permissions:
            return True
        return False


    