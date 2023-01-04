from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from src.sale.models import SaleDetail
from src.purchase.models import PurchaseDetail
from src.custom_lib.serializers.stock_serializers import PurchaseDetailStockSerializer, StockAnalysisSerializer, OrderAnalysisSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend, DateFromToRangeFilter
from src.item.models import Item
from src.custom_lib.functions.stock import get_item_ledger
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import generics
from django.utils import timezone
import django_filters
from rest_framework.permissions import BasePermission, SAFE_METHODS
from src.custom_lib.functions import stock
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import FilterSet
import django_filters
from src.core_app.pagination import CustomPagination
from rest_framework.pagination import LimitOffsetPagination
from django.db.models import Q
from ..serializers.stock_serializers import ItemStockListSerializer


from django.core.paginator import Paginator
from django.db.models import F, Q
from django.db import models

class FilterForPurchaseDetailStock(django_filters.FilterSet):
    date = django_filters.DateFromToRangeFilter(field_name="created_date_ad")
    class Meta:
        model = PurchaseDetail
        fields = ['id', 'purchase_main',  'item']


class PurchaseDetailStockViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PurchaseDetail.objects.filter(ref_purchase_detail__isnull=True)
    serializer_class = PurchaseDetailStockSerializer
    filter_class = FilterForPurchaseDetailStock 
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    ordering_fields = ['id', 'item__brand_name']
    search_fields = ['item__brand_name','item__code']


    # def list(self, request):
    #     remaining_qty = PurchaseDetail.objects.filter(remaining_qty__gt=0.00)
    #     return Response(remaining_qty, status=status.HTTP_200_OK)
  

# class StockAnalysisPermission(BasePermission):
#     def has_permission(self, request, view):
#         if request.user.is_anonymous:
#             return False
#         if request.user.is_superuser is True:
#             return True
#         try:
#             user_permissions = request.user.group.permissions.values_list('code_name', flat=True)
#         except:
#             return False
#         if request.method in SAFE_METHODS and 'view_stock_analysis' in user_permissions:
#             return True
#         return False


class StockAnalysisView(viewsets.ReadOnlyModelViewSet):
    # permission_classes = [StockAnalysisPermission]
    queryset = Item.objects.filter(purchasedetail__isnull=False).distinct()
    serializer_class = StockAnalysisSerializer
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    search_fields = ['brand_name', 'code']
    ordering_fields = ['id']
    filter_fields = ['id', 'brand_name' ]
    pagination_class = LimitOffsetPagination


class GetStockByItemBillingView(viewsets.ReadOnlyModelViewSet):
    # permission_classes = [StockAnalysisPermission]
    queryset = Item.objects.filter(purchasedetail__isnull=False).distinct()
    serializer_class = StockAnalysisSerializer
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    search_fields = ['brand_name', 'code']
    ordering_fields = ['id']
    filter_fields = {
        'id': ["in", "exact"], # note the 'in' field
        'brand_name': ["exact"]
    }
   

class OrderAnalysisView(viewsets.ReadOnlyModelViewSet):
    # permission_classes = [StockAnalysisPermission]
    queryset = Item.objects.filter(Q(purchasedetail__isnull=False) | Q(orderdetail__isnull=False)).distinct()
    serializer_class = OrderAnalysisSerializer
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    search_fields = ['brand_name', 'code']
    ordering_fields = ['id']
    filter_fields = ['id', 'brand_name' ]

class ListItemsForStockAnalysis(viewsets.ReadOnlyModelViewSet):
    queryset = Item.objects.filter(active=True)
    serializer_class = ItemStockListSerializer
    pagination_class = CustomPagination
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ['brand_name']
    filter_fields = ['id']
    ordering_fields = ['id', 'brand_name']



class ItemLedgerPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        if request.user.is_superuser is True:
            return True
        try:
            user_permissions = request.user.group.permissions.values_list('code_name', flat=True)
        except:
            return False
        if request.method in SAFE_METHODS and 'view_item_ledger' in user_permissions:
            return True
        return False



class  FilterForItemLedger(FilterSet):
    
    date = DateFromToRangeFilter(field_name="created_date_ad")
  
    class Meta:
        model = PurchaseDetail
        fields =['purchase_main__supplier', 'amount', 'qty','item']

# class ItemLedgerView(ListAPIView):
#     page_size = 10

#     def get(self,request):
#         foo =  PurchaseDetail.objects.all().values('created_date_ad', 'created_date_bs', 'qty') \
#         .annotate(item_name=F('item__brand_name'),
#                   item=F('item'),
#                   supplier_customer_name=F('purchase_main__supplier__name'),
#                   supplier_customer=F('purchase_main__supplier'),
#                   amount=F('amount'),
                  
#                   op_type=Case(
#                       When(purchase_main__purchase_type=1, then=Value('PURCHASE')),
#                       When(purchase_main__purchase_type=2, then=Value('PURCHASE-RETURN')),
#                       When(purchase_main__purchase_type=3, then=Value('OPENING-STOCK')),
#                       default=Value('N/A'),
#                       output_field=models.CharField()))\
#         .union(SaleDetail.objects.all().values('created_date_ad', 'created_date_bs', 'qty') \
#                .annotate(item_name=F('item__brand_name'),
#                          item=F('item'),
#                          supplier_customer_name=F('sale_main__customer__first_name'),
#                          supplier_customer=F('sale_main__customer'),
#                          amount=F('amount'),
#                          op_type=Case(
#                              When(sale_main__sale_type=1, then=Value('SALE')),
#                              When(sale_main__sale_type=2, then=Value('SALE-RETURN')),
#                              default=Value('N/A'),
#                              output_field=models.CharField(),
#                              ),

#                          ), all=True)
#         print(foo,"this is this")
#         paginator = PageNumberPagination()
#         paginator.page_size = 10
#         result_page = paginator.paginate_queryset(foo, request)
#         print(result_page,"this is data")
#         # serializer = ItemLedgerSerializer(result_page, many=True)
#         return paginator.get_paginated_response(result_page)

class ItemLedgerView(APIView):
    permission_classes = [ItemLedgerPermission]
    queryset = PurchaseDetail.objects.all()
    # pagination_class= CustomPagination
    # pagination_class = CustomLimitOffsetPagination

    # def get_paginated_response(self, data):
    #     response = Response(data)
    #     response['count'] = self.page.paginator.count
    #     response['next'] = self.get_next_link()
    #     response['previous'] = self.get_previous_link()
    #     return response

    def get(self, request):
        query_dict = {

        }
        for k, vals in request.GET.lists():
            if vals[0] != '':
                k = str(k)
                if k == 'date_after':
                    k = 'created_date_ad__date__gte'
                elif k == 'date_before':
                    k = 'created_date_ad__date__lte'
                query_dict[k] = vals[0]
        data = get_item_ledger(query_dict)
        return Response(data, status=status.HTTP_200_OK)

       
  
# class ExpiredItemReportPermission(BasePermission):
#     def has_permission(self, request, view):
#         if request.user.is_anonymous:
#             return False
#         if request.user.is_superuser is True:
#             return True
#         try:
#             user_permissions = request.user.group.permissions.values_list('code_name', flat=True)
#         except:
#             return False
#         if request.method in SAFE_METHODS and 'view_expired_item_report' in user_permissions:
#             return True
#         return False


# class ExpiredItemView(viewsets.ReadOnlyModelViewSet):
#     permission_classes = [ExpiredItemReportPermission]
#     queryset = PurchaseDetail.objects.filter(ref_purchase_detail__isnull=True)
#     serializer_class = PurchaseDetailStockSerializer
#     filter_class = FilterForPurchaseDetailStock
#     filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
#     ordering_fields = ['id']
#     search_fields = ['item__brand_name']
#     filter_fields = ['id', 'purchase_main', 'purchase_main__supplier', 'item']
