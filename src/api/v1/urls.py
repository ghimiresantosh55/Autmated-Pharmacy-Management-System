'''
Urls path for App
'''
from django.urls import path, include
from src.custom_lib.views.stock_views import StockAnalysisView, GetStockByItemBillingView
# from rest_framework import routers

from django.urls import path, include
from src.custom_lib.views.stock_views import ListItemsForStockAnalysis, StockAnalysisView, OrderAnalysisView, ItemLedgerView
from src.custom_lib.list_apis.views import ItemListView
# router = routers.DefaultRouter(trailing_slash=False)

# router.register("item-ledger",  ItemLedgerView)
urlpatterns = [

    path('user-app/', include('src.user.urls')),
    path('group-app/', include('src.user_group.urls')),
    path('core-app/', include('src.core_app.urls')),
    path('item-app/', include('src.item.urls')),
    path('company-app/', include('src.company.urls')),
    path('supplier-app/', include('src.supplier.urls')),
    path('customer-app/', include('src.customer.urls')),
    path('customer-order-app/', include('src.customer_order.urls')),
    path('purchase-order-app/', include('src.purchase_order.urls')),
    path('purchase-app/', include('src.purchase.urls')),
    path('financial-report-app/', include('src.financial_report.urls')),
    path('store-app/', include('src.store.urls')),
    path('sale-app/', include('src.sale.urls')),
    path('mobile-sms/', include('src.mobile_sms.urls')),
    path("stock-app/get-stock-by-item", StockAnalysisView.as_view({'get': 'list'}), name="get_stock_by_item"),
    path("stock-app/get-stock-by-item-billing", GetStockByItemBillingView.as_view({'get': 'list'}), name="get_stock_by_item-billing"),
    path('stock-app/stock-analysis', StockAnalysisView.as_view({'get': 'list'})),
    path('stock-app/order-analysis', OrderAnalysisView.as_view({'get': 'list'})),
    path('stock-app/item', ListItemsForStockAnalysis.as_view({'get': 'list'})),
    path('stock-app/item-ledger', ItemLedgerView.as_view()),
    path("stock-app/item-ledger/item-list", ItemListView.as_view()),
    path('credit-management-app/', include('src.credit_management.urls')),
    path('party-payment-app/', include('src.party_payment.urls')),
    path('public-app/', include('src.public.urls')),
    path('blood-test-order-app/', include('src.blood_test_order.urls')),
    path('blood-test-app/', include('src.blood_test.urls')),
    
   
  
  
]
