
'''
routing urls for sale api
'''
from rest_framework import routers
from django.urls import path, include
from .views import SaveSaleViewSet,  ListSaleMainViewSet, ReturnSaleView, SaleDetailForReturnViewSet
from src.item.views import  GetItemDataViewSet

router = routers.DefaultRouter(trailing_slash=False)

router.register("sale", ListSaleMainViewSet)
router.register("save-sale", SaveSaleViewSet)
router.register('return-sale',  ReturnSaleView)
router.register("get-item-data",  GetItemDataViewSet)
router.register("get-sale-info", SaleDetailForReturnViewSet)
# router.register("sale-payment-detail", SalePaymentDetailView)

urlpatterns = [
    path('', include(router.urls))
]