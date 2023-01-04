from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from src.sale.models import SaleMain
from src.financial_report.serializers.SaleSerializer import SaleGetDataSerializer, SaleMainSummarySerializer, SaleMainReportSerializer
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend, DateFromToRangeFilter
from rest_framework.response import Response
from rest_framework import status
from src.customer.models import Customer
from src.customer_order.serializers import GetUserSerializer
from src.user.models import User

class SearchAndOrderingFields:
    search_fields = ['id']
    ordering_fields = ['id',]
    

class SaleReportFilter(filters.FilterSet):
    date = DateFromToRangeFilter(field_name="created_date_ad")
    class Meta:
        model = SaleMain
        fields = "__all__"

class SaleReportDetailViewSet(ReadOnlyModelViewSet):
    queryset = SaleMain.objects.prefetch_related('sale_details').all()
    serializer_class = SaleMainReportSerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = SearchAndOrderingFields.search_fields
    ordering_fields = SearchAndOrderingFields.ordering_fields
    filterset_class = SaleReportFilter


class SaleReportSummaryViewSet(ReadOnlyModelViewSet):
    queryset = SaleMain.objects.all()
    serializer_class = SaleMainSummarySerializer
    filter_backends = (SearchFilter, OrderingFilter, filters.DjangoFilterBackend)
    search_fields = SearchAndOrderingFields.search_fields
    ordering_fields = SearchAndOrderingFields.ordering_fields
    filterset_class = SaleReportFilter
    


class SaleGetDataView(ListAPIView):
    serializer_class = SaleGetDataSerializer
    customers = Customer.objects.none()


    def list(self, request, *args, **kwargs):
        customers = Customer.objects.values("id", "first_name", "last_name")
        users = User.objects.filter(active=True, user_type =1)
        user_serializer = GetUserSerializer(users, many=True)
        # print(customers)
    
        data = {
            "filter_fields": list(SaleReportFilter.get_fields().keys()),
            "search_fields": SearchAndOrderingFields.search_fields,
            "ordering_fields": SearchAndOrderingFields.ordering_fields,
            "customers": customers,
            "users":users,
        }
        data['users'] = user_serializer.data
        serializer = self.serializer_class(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

