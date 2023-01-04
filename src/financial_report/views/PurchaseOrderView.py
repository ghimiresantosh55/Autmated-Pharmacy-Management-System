
from rest_framework import  viewsets, status
from rest_framework.response import Response
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from src.purchase_order.models import PurchaseOrderMain, PurchaseOrderDetail
from src.supplier.models import Supplier
from src.financial_report.serializers.PurchaseOrderSerializer import  PurchaseOrderMainReportSerializer,  SummaryPurchaseOrderMainSerializer, PurchaseOrderGetDataSerializer, SupplierReportSerializer
from src.financial_report.permissions.purchase_order_permission import PurchaseOrderReportPermission
from rest_framework.generics import ListAPIView
from src.customer_order.serializers import GetUserSerializer
from src.user.models import User



class SearchAndOrderingFields:
    search_fields = ['id']
    ordering_fields = ['id',]


class PurchaseOrderReportFilter(filters.FilterSet):
    data = filters.DateFromToRangeFilter(field_name="created_date_aad")
    class Meta:
        model = PurchaseOrderMain
        fields = "__all__"


class PurchaseOrderDetailReportViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [PurchaseOrderReportPermission]
    queryset = PurchaseOrderMain.objects.all().prefetch_related('purchase_order_details').all()
    serializer_class =  PurchaseOrderMainReportSerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = SearchAndOrderingFields.search_fields
    ordering_fields = SearchAndOrderingFields.ordering_fields 
    filterset_class =  PurchaseOrderReportFilter



class PurchaseOrderSummaryReportViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [PurchaseOrderReportPermission]
    queryset = PurchaseOrderMain.objects.all()
    serializer_class = SummaryPurchaseOrderMainSerializer
    filter_class =  PurchaseOrderReportFilter
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = SearchAndOrderingFields.ordering_fields
    ordering_fields = SearchAndOrderingFields.ordering_fields



class PurchaseOrderReportGetDataView(ListAPIView):
    serializer_class = PurchaseOrderGetDataSerializer
    suppliers = Supplier.objects.none()

    def list(self, request, *args, **kwargs):
        suppliers = Supplier.objects.values("id", "name", "address","phone_no")
        users = User.objects.filter(active=True, user_type =1)
        user_serializer = GetUserSerializer(users, many=True)
        #
    
        data = {
            "filter_fields": list(PurchaseOrderReportFilter.get_fields().keys()),
            "search_fields": SearchAndOrderingFields.search_fields,
            "ordering_fields": SearchAndOrderingFields.ordering_fields,
            "suppliers": suppliers,
            "users":users,
        }
        data['users'] = user_serializer.data
        serializer = self.serializer_class(data)
        return Response(serializer.data, status=status.HTTP_200_OK)
