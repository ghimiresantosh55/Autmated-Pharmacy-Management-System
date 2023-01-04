from rest_framework import routers

from django.urls import path, include

from .views import CreditInvoice, CreditClearanceViewSet, CreditClearanceViewSet,  GetReceiptDataCustomerWise, CreditClearanceSummary

router = routers.DefaultRouter(trailing_slash=False)
# router.register("credit-clearance-payment-detail", CreditPaymentDetailViewSet)
router.register("credit-clearance-summary", CreditClearanceSummary)
router.register("credit-invoice", CreditInvoice)
router.register("credit-clearance", CreditClearanceViewSet)
router.register("get-receipt-data",  GetReceiptDataCustomerWise)

urlpatterns = [
     path('', include(router.urls))
]
