'''
Urls for core app
'''
from rest_framework import routers
from django.urls import path, include
from .views import OrganizationSetupViewSet, OrganizationRuleViewSet, PaymentModeViewSet,  CheckUniqueUserViewSet,\
    AppAccessLogViewset


router = routers.DefaultRouter(trailing_slash=False)
router.register("organization-setup", OrganizationSetupViewSet)
router.register("organization-rule", OrganizationRuleViewSet)
router.register("app-access-log", AppAccessLogViewset)
router.register("payment-mode", PaymentModeViewSet)
router.register("check-unique-user", CheckUniqueUserViewSet)

urlpatterns = [
    path('', include(router.urls))
]
