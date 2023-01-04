import django_filters
from rest_framework import  viewsets, status
from rest_framework.response import Response
from django.core import serializers
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend, DateFromToRangeFilter
from rest_framework.filters import OrderingFilter, SearchFilter
from src.purchase.models import PurchaseMain, PurchaseDetail
from src.supplier.models import Supplier
from src.financial_report.serializers.PurchaseSerializer import  PurchaseMainReportSerializer,  SummaryPurchaseMainSerializer, PurchaseGetDataSerializer, SupplierReportSerializer
from src.financial_report.permissions.purchase_permission import PurchaseReportPermission
from rest_framework.generics import ListAPIView
from src.customer_order.serializers import GetUserSerializer
from src.user.models import User



class SearchAndOrderingFields:
    search_fields = ['id']
    ordering_fields = ['id',]

class PurchaseReportFilter(filters.FilterSet):
    date = DateFromToRangeFilter(field_name="created_date_ad")
    class Meta:
        model = PurchaseMain
        fields = "__all__"

class PurchaseDetailReportViewSet(viewsets.ReadOnlyModelViewSet):
    # permission_classes = [PurchaseOrderReportPermission]
    queryset = PurchaseMain.objects.all().prefetch_related('purchase_details').all()
    serializer_class =  PurchaseMainReportSerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = SearchAndOrderingFields.search_fields
    ordering_fields = SearchAndOrderingFields.ordering_fields 
    filterset_class =  PurchaseReportFilter



class PurchaseSummaryReportViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [PurchaseReportPermission]
    queryset = PurchaseMain.objects.all()
    serializer_class = SummaryPurchaseMainSerializer
    filter_class =  PurchaseReportFilter
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = SearchAndOrderingFields.ordering_fields
    ordering_fields = SearchAndOrderingFields.ordering_fields



class PurchaseReportGetDataView(ListAPIView):
    serializer_class = PurchaseGetDataSerializer
    suppliers = Supplier.objects.none()


    def list(self, request, *args, **kwargs):
        suppliers = Supplier.objects.values("id", "name", "address","phone_no")
        users = User.objects.filter(active=True, user_type =1)
        user_serializer = GetUserSerializer(users, many=True)
        #
    
        data = {
            "filter_fields": list(PurchaseReportFilter.get_fields().keys()),
            "search_fields": SearchAndOrderingFields.search_fields,
            "ordering_fields": SearchAndOrderingFields.ordering_fields,
            "suppliers": suppliers,
            "users":users,
        }
        data['users'] = user_serializer.data
        serializer = self.serializer_class(data)
        return Response(serializer.data, status=status.HTTP_200_OK)
