from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from src.customer_order.models import OrderMain
from src.financial_report.serializers.CustomerOrderSerializer import CustomerOrderMainReportSerializer, CustomerOrderMainSummarySerializer, CustomerOrderGetDataSerializer
from src.user.models import  User
from src.customer_order.serializers import GetUserSerializer
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db import connection
from rest_framework.response import Response
from rest_framework import status
from src.customer.models import Customer
from django.db import connection

class SearchAndOrderingFields:
    search_fields = ['id']
    ordering_fields = ['id',]
    

class CustomerOrderReportFilter(filters.FilterSet):
    date = filters.DateFromToRangeFilter(field_name="created_date_ad")
    class Meta:
        model = OrderMain
        fields = "__all__"

class CustomerOrderReportDetailViewSet(ReadOnlyModelViewSet):
    queryset = OrderMain.objects.prefetch_related('order_details').all()
    serializer_class = CustomerOrderMainReportSerializer
    filter_backends = (SearchFilter, OrderingFilter, filters.DjangoFilterBackend)
    search_fields = SearchAndOrderingFields.search_fields
    ordering_fields = SearchAndOrderingFields.ordering_fields
    filterset_class = CustomerOrderReportFilter


class CustomerOrderReportSummaryViewSet(ReadOnlyModelViewSet):
    queryset = OrderMain.objects.all()
    serializer_class = CustomerOrderMainSummarySerializer
    filter_backends = (SearchFilter, OrderingFilter, filters.DjangoFilterBackend)
    search_fields = SearchAndOrderingFields.search_fields
    ordering_fields = SearchAndOrderingFields.ordering_fields
    filterset_class = CustomerOrderReportFilter
    


class CustomerOrderReportGetDataView(ListAPIView):
    serializer_class = CustomerOrderGetDataSerializer
    customers = Customer.objects.none()

  
    def list(self, request, *args, **kwargs):

        customers = Customer.objects.all()
        users = User.objects.filter(active=True, user_type =1)
        user_serializer = GetUserSerializer(users, many=True)
        # print(customers)
    
        data = {
            "filter_fields": list(CustomerOrderReportFilter.get_fields().keys()),
            "search_fields": SearchAndOrderingFields.search_fields,
            "ordering_fields": SearchAndOrderingFields.ordering_fields,
            "customers": customers,
            "users":users,
           
        }
        data['users'] = user_serializer.data
        serializer = self.serializer_class(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

