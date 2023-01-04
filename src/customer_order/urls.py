'''
routing urls for customer order api
'''
from rest_framework import routers

from django.urls import path, include
from .views import  SaveOrderMainViewSet, OrderDetailViewSet , OrderMainViewSet,\
     CustomerOrderMainDispatchViewSet, DeleteCustomerOrderViewSet, OrderMainBulkUpdate, AmountStatusBulkUpdate
       
        
from src.item.views import  GetItemDataViewSet

router = routers.DefaultRouter(trailing_slash=False)

# Check where this URL is used???
router.register("save-customer-order", SaveOrderMainViewSet)
router.register("get-item-data",  GetItemDataViewSet)
router.register("order-detail", OrderDetailViewSet)
router.register("customer-order",  OrderMainViewSet)
router.register("customer-order-dispatch/update-delivery-status", CustomerOrderMainDispatchViewSet)
router.register("bulk-update-amount-status",  AmountStatusBulkUpdate)

urlpatterns = [
    path('order-detail/<int:pk>', DeleteCustomerOrderViewSet.as_view()),
    path('bulk-update-order-main', OrderMainBulkUpdate.as_view()),
  

] + router.urls
