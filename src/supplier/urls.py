'''
routing urls for supplier url
'''
from rest_framework import routers
from django.urls import path, include
from .views import SupplierViewSet, SupplierContactViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register("supplier", SupplierViewSet)
router.register("supplier-contact", SupplierContactViewSet)


urlpatterns = [
    path('', include(router.urls))
]