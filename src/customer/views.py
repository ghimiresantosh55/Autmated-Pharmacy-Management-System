# third-party
from .password_generator import random_password_generator
from django.db import transaction

from rest_framework import serializers, viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
import django_filters
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
# imported serializers
from .serializers import CustomerListSerializer, RegisterCustomerSerializer, UpdateCustomerSerializer
from rest_framework.permissions import AllowAny

# imported models
from .models import Customer
from rest_framework.views import APIView
from .serializers import RegisterCustomerSerializer
#importing permission
from .customer_permissions import CustomerPermission, CustomerUpdatePermissions
from simple_history.utils import update_change_reason
from src.core_app.pagination import CustomPagination



class FilterForCustomer(django_filters.FilterSet):
    '''
    custom filter for customer
    '''
    date = django_filters.DateFromToRangeFilter(field_name="created_date_ad")
    first_name = django_filters.CharFilter(field_name="first_name", lookup_expr='iexact')
   
    class Meta:
        model = Customer
        fields = ['first_name', 'user__email', 'id','home_address','phone_no']

class CustomerViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    Readonly model viewset for customer
    '''
    permission_classes = [CustomerPermission]
    queryset = Customer.objects.all().order_by('id')
    serializer_class = CustomerListSerializer
    filter_class =  FilterForCustomer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ['first_name', 'phone_no','user__email', 'id']
    ordering_fields = ['first_name', ]
    # pagination_class = CustomPagination


class CustomerRegisterView(viewsets.ModelViewSet):
    '''
    Model viewset for customer register
    '''
    permission_classes =  [AllowAny]
    queryset = Customer.objects.all()
    http_method_names = ['post']
    serializer_class = RegisterCustomerSerializer

    @transaction.atomic
    def create(self, request):
        '''
        method for create or register customer
        '''
        if request.data['user']['password']== "" or request.data['user']['password'] is None:
            generatered_password = random_password_generator(upper_case=True, numbers=True)
            request.data['user']['password'] = generatered_password
            request.data['user']['confirm_password'] = generatered_password

        if request.data['user']['user_name']=="" or request.data['user']['user_name'] is None:
            request.data['user']['user_name']= request.data['phone_no']
        
        if request.data['user']['email']=="" or request.data['user']['email'] is None:
            request.data['user']['email']= request.data['phone_no']+ "@gmail.com"
        
        

        serializer = RegisterCustomerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class FilterForCustomerUpdate(django_filters.FilterSet):
    '''
    custom filter for customer update
    '''
    date = django_filters.DateFromToRangeFilter(field_name="created_date_ad")
    first_name = django_filters.CharFilter(field_name="first_name", lookup_expr='iexact')
   
    class Meta:
        model = Customer
        fields = ['id', 'user__user_name', 'user__email', 'phone_no','first_name','last_name']

class CustomerUpdateView(viewsets.ModelViewSet):
    '''
    Model viewset for customer update
    '''
    permission_classes = [CustomerUpdatePermissions]
    queryset = Customer.objects.all()
    http_method_names = ['patch', 'get']
    serializer_class = UpdateCustomerSerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    filter_class = FilterForCustomerUpdate
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ['phone_no','user__user_name']
    ordering_fields = [ 'first_name', ]

    
    
    def partial_update(self, request, pk , *args, **kwargs):
        '''
        Partial Update Method For Customer
        '''
        try:
            remarks = str(request.data['remarks']).strip()
            if len(remarks) <= 0:
                return Response({'remarks': 'Please give at least one word for remarks'},
                                status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'remarks': 'Please Provide remarks'}, status=status.HTTP_400_BAD_REQUEST)

        if request.data['user']['password']== "" or request.data['user']['password'] is None:
            generatered_password = random_password_generator(upper_case=True, numbers=True)
            request.data['user']['password'] = generatered_password
            request.data['user']['confirm_password'] = generatered_password

        if request.data['user']['user_name']=="" or request.data['user']['user_name'] is None:
            request.data['user']['user_name']= request.data['phone_no']
        
        if request.data['user']['email']=="" or request.data['user']['email'] is None:
            request.data['user']['email']= request.data['phone_no']+ "@gmail.com"
            
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True, context={'request': request,
                                                                                                 'pk': instance.user.id}) 
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            '''
            for log history. Atleast one reason must be given if update is made
            '''
            update_change_reason(instance, remarks)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  

    

