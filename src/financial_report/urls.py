from django.urls import path
from rest_framework.routers import DefaultRouter
from .views.CustomerOrderViews import CustomerOrderReportDetailViewSet, CustomerOrderReportSummaryViewSet, CustomerOrderReportGetDataView
from .views.PurchaseOrderView import PurchaseOrderSummaryReportViewSet, PurchaseOrderDetailReportViewSet, PurchaseOrderReportGetDataView
from .views.PurchaseOrderReceivedView import PurchaseOrderReceivedSummaryReportViewSet, PurchaseOrderReceivedDetailReportViewSet, PurchaseOrderReceivedReportGetDataView
from .views.PurchaseView import PurchaseDetailReportViewSet, PurchaseReportGetDataView, PurchaseSummaryReportViewSet
from .views.SaleView import SaleReportSummaryViewSet, SaleReportDetailViewSet, SaleGetDataView


router = DefaultRouter(trailing_slash=False)
router.register("customer-order/detail", CustomerOrderReportDetailViewSet, basename="customer-order-report-detail")
router.register("customer-order/summary", CustomerOrderReportSummaryViewSet, basename="customer-order-report-summary")

router.register("purchase-order/summary", PurchaseOrderSummaryReportViewSet, basename="purchase-order-report-summary")
router.register("purchase-order/detail",  PurchaseOrderDetailReportViewSet, basename="purchase-order-report-detail")

router.register("purchase-order-receive/summary", PurchaseOrderReceivedSummaryReportViewSet, basename="purchase-order-receive-report-summary")
router.register("purchase-order-receive/detail",  PurchaseOrderReceivedDetailReportViewSet, basename="purchase-order-receive-report-detail")

router.register("purchase/summary", PurchaseSummaryReportViewSet, basename="purchase-report-summary")
router.register("purchase/detail",  PurchaseDetailReportViewSet, basename="purchase-report-detail")

router.register("sale/summary", SaleReportSummaryViewSet, basename="sale-report-summary")
router.register("sale/detail",  SaleReportDetailViewSet, basename="sale-report-detail")

urlpatterns = [
    path("customer-order/get-data", CustomerOrderReportGetDataView.as_view(), name="customer-order-report-get-data"),
    path("purchase-order/get-data", PurchaseOrderReportGetDataView.as_view(), name="purchase-order-report-get-data"),
    path("purchase-order-receive/get-data", PurchaseOrderReceivedReportGetDataView.as_view(), name="purchase-order-receive-report-get-data"),
    path("purchase/get-data", PurchaseReportGetDataView.as_view(), name="purchase-report-get-data"),
    path("sale/get-data", SaleGetDataView.as_view(), name="sale-get-data")
       
] + router.urls
