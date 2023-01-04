'''
routing urls for purchase order api
'''
from rest_framework.urls import path
from rest_framework import routers
from .po_received_views import POReceivedViewSet
from .views import ListPurchaseOrderMainViewSet, SavePurchaseOrderView, ListPurchaseOrderReceivedMainViewSet, QuickUpdatePurchaseOrderMainViewSet,  DeletePurchaseOrderReceivedViewSet
from src.item.views import  GetItemDataViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register("purchase-order", ListPurchaseOrderMainViewSet)
router.register("save-purchase-order", SavePurchaseOrderView)
router.register("purchase-order-received", ListPurchaseOrderReceivedMainViewSet)
router.register("update-purchase-order",  QuickUpdatePurchaseOrderMainViewSet)
router.register("get-item-data",  GetItemDataViewSet)

urlpatterns = [
    path("save-purchase-order-received", POReceivedViewSet.as_view(), name="create purchase order receive"),
    path('purchase-order-received-detail/<int:pk>', DeletePurchaseOrderReceivedViewSet.as_view())
] + router.urls
