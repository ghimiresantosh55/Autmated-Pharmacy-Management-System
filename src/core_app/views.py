'''
model viewset  class for core app
'''

from rest_framework import viewsets, status
#importing of models
from .models import OrganizationSetup, OrganizationRule,  AppAccessLog, PaymentMode
from src.user.models import User

# importing of serializers
from .serializers import OrganizationRuleSerializer, OrganizationSetupSerializer, PaymentModeSerializer, CheckUniqueUserSerializer

from .serializers import  AppAccessLogSerializer
from django_filters.filterset import FilterSet
from rest_framework.response import Response

# filter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
import django_filters
from django_filters import DateFromToRangeFilter

# permissions
from .core_app_permissions import OrganizationRulePermission, OrganizationSetupPermission, PaymentModePermission
from src.user.user_permissions import UserViewPermissions
from simple_history.utils import update_change_reason



class OrganizationRuleViewSet(viewsets.ModelViewSet):
    '''
    model viewset for organization rule
    '''

    '''
    addition of permission
    '''
    permission_classes = [OrganizationRulePermission]
    '''
    objects.all() helps to get all the object from table (i.e. model)
    '''
    queryset = OrganizationRule.objects.all()
    serializer_class = OrganizationRuleSerializer
    '''
    helps to control http method
    '''
    http_method_names = ['get', 'head', 'post', 'patch']


    def partial_update(self, request, *args, **kwargs):
        '''
        exception handling
        '''
        '''
        first try block is executed if condition doesnot match error is passed.
        '''
        try:
            remarks = str(request.data['remarks']).strip()
            if len(remarks) <= 0:
                return Response({'remarks': 'Please give at least one word for remarks'}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'remarks': 'Please Provide remarks'}, status=status.HTTP_400_BAD_REQUEST)
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            '''
            for log history. Atleast one reason must be given if update is made
            '''
            update_change_reason(instance, remarks)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class OrganizationSetupViewSet(viewsets.ModelViewSet):
    '''
    model viewset class for organization setup
    '''

    '''
    addition of permission
    '''
    permission_classes = [OrganizationSetupPermission]
    '''
    objects.all() helps to get all the object from table (i.e. model)
    '''
    queryset = OrganizationSetup.objects.all()
    serializer_class = OrganizationSetupSerializer
    '''
    helps to control http method
    '''
    http_method_names = ['get', 'head', 'post', 'patch']
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['id', 'name', 'address', 'email', 'created_date_ad']
    filter_fields = ['name', 'address', 'email', 'created_date_ad']
    search_fields = ['name', 'address', 'email', 'created_date_ad']

    def partial_update(self, request, *args, **kwargs):
        '''
        exception handling
        '''
        '''
        first try block is executed if condition doesnot match error is passed.
        '''
        try:
            remarks = str(request.data['remarks']).strip()
            if len(remarks) <= 0:
                return Response({'remarks': 'Please give at least one word for remarks'},
                                status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'remarks': 'Please Provide remarks'}, status=status.HTTP_400_BAD_REQUEST)
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            '''
            for log history. Atleast one reason must be given if update is made
            '''
            update_change_reason(instance, remarks)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class FilterForAppAccessLog(FilterSet):
    '''
    custom filter for app access log
    '''
    date = DateFromToRangeFilter(field_name="created_date_ad")
    class Meta:
        model = AppAccessLog
        fields = "__all__"

class AppAccessLogViewset(viewsets.ModelViewSet):

    '''
    objects.all() helps to get all the object from table (i.e. model)
    '''
    queryset = AppAccessLog.objects.all()
    # permission_classes = [AppAccessLogPermission]
    serializer_class = AppAccessLogSerializer
    '''
    helps to control http method
    '''
    http_method_names = ['get', 'head', 'post']

    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filter_class = FilterForAppAccessLog
    ordering_fields = ['id']
    search_fields = ['app_type','device_type']
   



class FilterForPaymentMode(FilterSet):
    date = DateFromToRangeFilter(field_name="created_date_ad")
    name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = PaymentMode
        fields = ['active',]


class PaymentModeViewSet(viewsets.ModelViewSet):
    permission_classes = [PaymentModePermission]
    queryset = PaymentMode.objects.all()
    serializer_class = PaymentModeSerializer
    http_method_names = ['get', 'head', 'post', 'patch']
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['id', 'name']
    filter_class = FilterForPaymentMode
    search_fields = ['name', 'remarks']

    def partial_update(self, request, *args, **kwargs):
        try:
            remarks = str(request.data['remarks']).strip()
            if len(remarks) <= 0:
                return Response({'remarks': 'Please give at least one word for remarks'},
                                status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'remarks': 'Please Provide remarks'}, status=status.HTTP_400_BAD_REQUEST)
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            update_change_reason(instance, remarks)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class FilterForUniqueUser(FilterSet):
    date = DateFromToRangeFilter(field_name="created_date_ad")
    user_name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = User
        fields = ['user_name','email']

class CheckUniqueUserViewSet(viewsets.ModelViewSet):
    permission_classes = [UserViewPermissions]
    queryset = User.objects.all()
    serializer_class = CheckUniqueUserSerializer
    http_method_names = ['get', ]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    ordering_fields = ["user_name" ,]
    filter_class = FilterForUniqueUser
    search_fields = ['user_name', ]