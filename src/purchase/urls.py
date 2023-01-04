'''
routing urls for purchase api
'''
from rest_framework import routers
from django.urls import path, include
from .views import  ListPurchaseMainViewSet, VerifyPurchaseOrderView,  SaveOpeningStockViewset, ReturnPurchaseView, UpdatePurchaseDetailViewSet,\
    DirectPurchaseView
    
from src.custom_lib.views.stock_views import PurchaseDetailStockViewSet
from src.item.views import  GetItemDataViewSet

router = routers.DefaultRouter(trailing_slash=False)

router.register("purchase", ListPurchaseMainViewSet)
router.register("verify-purchase-order-received", VerifyPurchaseOrderView)
router.register('save-opening-stock', SaveOpeningStockViewset)
router.register('get-stock-by-purchase', PurchaseDetailStockViewSet)
router.register('return-purchase', ReturnPurchaseView)
router.register('purchase-detail-update', UpdatePurchaseDetailViewSet)
router.register("get-item-data",  GetItemDataViewSet)
router.register("direct-purchase",  DirectPurchaseView)

urlpatterns = [
    path('', include(router.urls))
]