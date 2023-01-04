  
from rest_framework import routers

from django.urls import path, include

from .views import SavePartyPaymentViewSet,  GetPartyInvoice,\
      PartyPaymentSummaryViewSet, GetReceiptDataSupplierWise

router = routers.DefaultRouter(trailing_slash=False)
# router.register("party-payment", PartyPaymentViewSet)
# router.register("party-payment-payment-detail", PartyPaymentDetailViewSet)
router.register("party-payment-summary", PartyPaymentSummaryViewSet)
router.register("party-payment", SavePartyPaymentViewSet)
router.register("party-invoice", GetPartyInvoice)
router.register("get-party-payment-data", GetReceiptDataSupplierWise)


urlpatterns = [
    path('', include(router.urls))
]
