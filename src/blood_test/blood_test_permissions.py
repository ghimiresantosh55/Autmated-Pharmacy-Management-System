
from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS


class BloodTestCategoryPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        if request.user.is_superuser is True:
            return True
        try:
            user_permissions = request.user.group.permissions.values_list('code_name', flat=True)
        except:
            return False
        if (request.method == 'POST' or request.method in SAFE_METHODS) and 'add_blood_test_category' in user_permissions:
            return True
        if request.method in SAFE_METHODS and 'view_blood_test_category' in user_permissions:
            return True
        if (request.method == 'PATCH' or request.method in SAFE_METHODS) and 'update_blood_test_category' in user_permissions:
            return True
        return False


class BloodTestPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        if request.user.is_superuser is True:
            return True
        try:
            user_permissions = request.user.group.permissions.values_list('code_name', flat=True)
        except:
            return False
        if (request.method == 'POST' or request.method in SAFE_METHODS) and 'add_blood_test' in user_permissions:
            return True
        if request.method in SAFE_METHODS and 'view_blood_test' in user_permissions:
            return True
        if (request.method == 'PATCH' or request.method in SAFE_METHODS) and 'update_blood_test' in user_permissions:
            return True
        return False


class TestPackagePermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        if request.user.is_superuser is True:
            return True
        try:
            user_permissions = request.user.group.permissions.values_list('code_name', flat=True)
        except:
            return False
        if (request.method == 'POST' or request.method in SAFE_METHODS) and 'add_test_package' in user_permissions:
            return True
        if request.method in SAFE_METHODS and 'view_test_package' in user_permissions:
            return True
        if (request.method == 'PATCH' or request.method in SAFE_METHODS) and 'update_test_package' in user_permissions:
            return True
        return False



        