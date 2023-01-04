'''
routing urls for customer api
'''
from rest_framework import routers
from django.urls import path, include
from src.customer.views import  CustomerRegisterView
from .views import CustomerViewSet,  CustomerUpdateView

router = routers.DefaultRouter(trailing_slash=False)
router.register("customer", CustomerViewSet)
router.register("register", CustomerRegisterView)
router.register("customer-update",  CustomerUpdateView)


urlpatterns = [
    path('', include(router.urls)),

]
