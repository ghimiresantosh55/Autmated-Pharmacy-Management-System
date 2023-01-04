from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS





class OrganizationRulePermission(BasePermission):
    def has_permission(self, request, view):
        # if unknown user then permission is denied
        if request.user.is_anonymous:
            return False

        # if user is superuser then permission is allowed.
        if request.user.is_superuser is True:
            return True

        # exception handling
        # first try block is checked if condition doesnot match error is passed
        try:
            # value from permissions model (i.e. code name) is saved in user_permissions
            user_permissions = request.user.group.permissions.values_list('code_name', flat=True)
        except:
            return False

        # add_organization_rule is checked in user_permissions if match permissions is provided for post operations
        if (request.method in SAFE_METHODS or request.method == 'POST') and 'add_organization_rule' in user_permissions:
            return True

        # view_organization_rule is checked in user_permissions if match permissions is provided for view operations
        if request.method in SAFE_METHODS and 'view_organization_rule' in user_permissions:
            return True

        # update_organization_rule is checked in user_permissions if match permissions is provided for update operations
        if (request.method in SAFE_METHODS or request.method == 'PATCH') and 'update_organization_rule' in user_permissions:
            return True
        return False


class OrganizationSetupPermission(BasePermission):
    def has_permission(self, request, view):
        # if unknown user then permission is denied
        if request.user.is_anonymous:
            return False
        
        # if user is superuser then permission is allowed.
        if request.user.is_superuser is True:
            return True
        user_permissions = request.user.group.permissions.values_list('code_name', flat=True)
        # add_organization_setup is checked in user_permissions if match permissions is provided for post operations
        if request.method == 'POST' and 'add_organization_setup' in user_permissions:
            return True
        if request.method in SAFE_METHODS and ('view_organization_setup' in user_permissions or
                                               'add_organization_setup' in user_permissions or
                                               'update_organization_setup' in user_permissions):
            return True
        # update_organization_setup is checked in user_permissions if match permissions is provided for update operations
        if request.method == 'PATCH' and 'update_organization_setup' in user_permissions:
            return True
        return False



class AppAccessLogPermission(BasePermission):
    def has_permission(self, request, view):
        # if user is unknown then permission is denied
        if request.user.is_anonymous:
            return False
        # if user is superuser then permission is allowed.
        if request.user.is_superuser is True:
            return True
        # exception handling
        # first try block is checked if condition doesnot match error is passed
        try:
            # value from permissions model (i.e. code name) is saved in user_permissions
            user_permissions = request.user.group.permissions.values_list('code_name', flat=True)
        except:
            return False
        
        # add_app_access_log is checked in user_permissions if match permissions is provided for add operations
        if (request.method == 'POST' or request.method in SAFE_METHODS) and 'add_app_access_log' in user_permissions:
            return True
        # view_app_access_log is checked in user_permissions if match permissions is provided for view operations
        if request.method in SAFE_METHODS and 'view_app_access_log' in user_permissions:
            return True
        return False



class PaymentModePermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        if request.user.is_superuser is True:
            return True
        user_permissions = request.user.group.permissions.values_list('code_name', flat=True)
        if request.method == 'POST' and 'add_payment_mode' in user_permissions:
            return True
        elif request.method in SAFE_METHODS and ('view_payment_mode' in user_permissions or
                                                 'add_payment_mode' in user_permissions or
                                                 'update_payment_mode' in user_permissions):
            return True
        elif request.method in SAFE_METHODS and 'approve_purchase_order' in user_permissions:
            return True
        elif request.method in SAFE_METHODS and 'add_purchase' in user_permissions:
            return True
        elif request.method in SAFE_METHODS and 'add_sale' in user_permissions:
            return True
        elif request.method in SAFE_METHODS and 'add_sale_return' in user_permissions:
            return True
        elif request.method == 'PATCH' and 'update_payment_mode' in user_permissions:
            return True
        return False