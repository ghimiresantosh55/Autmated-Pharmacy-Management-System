'''
views for user group
'''
# rest framework packages
from .serializers import CustomGroupSerializer, CustomPermissionSerializer, PermissionCategorySerializer
from .models import UserGroup, UserPermission, UserPermissionCategory
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter, SearchFilter

# django packages
from django_filters.rest_framework import DjangoFilterBackend, DateFromToRangeFilter, FilterSet
import django_filters
from django.shortcuts import render
from django.http import HttpResponse
from .group_permissions import GroupPermission, PermissionPermission, PermissionCategoryPermission


class FilterForCustomGroup(FilterSet):
    '''
    filter class for user group
    '''
    date = DateFromToRangeFilter(field_name="created_date_ad")
    name = django_filters.CharFilter(lookup_expr='iexact')
    class Meta:
        model = UserGroup
        fields = ['active', 'id',
                  'date', 'name']

class CustomGroupViewSet(ModelViewSet):
    '''
    viewset for custom group
    '''
    permission_classes = [GroupPermission]
    queryset = UserGroup.objects.all()
    serializer_class = CustomGroupSerializer
    filter_class = FilterForCustomGroup
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ['name']
    ordering_fields = ['id', 'name']


class CustomPermissionViewSet(ModelViewSet):
    '''
    viewset for custom permission
    '''
    permission_classes = [PermissionPermission]
    queryset = UserPermission.objects.all()
    serializer_class = CustomPermissionSerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ['name', 'code_name']
    ordering_fields = ['id', 'name']
    filter_fields = ['id', 'category']

    # def export(request):
    #     response = HttpResponse(content_type ='text/csv')

    #     writer = csv.writer(response)
    #     writer.writerow(['Id','Name', 'Code Name', 'Category', 'Created Date Ad','Created Date Bs','Created By'])


class PermissionCategoryViewSet(ModelViewSet):
    '''
    viewset for permission category
    '''
    permission_classes = [PermissionCategoryPermission]
    queryset = UserPermissionCategory.objects.all()
    serializer_class = PermissionCategorySerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ['name']
    ordering_fields = ['id', 'name']
    filter_fields = ['id']
