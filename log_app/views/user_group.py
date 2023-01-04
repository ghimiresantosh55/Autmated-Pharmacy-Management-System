from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
import django_filters
from django_filters import DateFromToRangeFilter
from rest_framework import permissions, viewsets
from django_filters.filterset import FilterSet
from src.user_group.models import  UserGroup, UserPermission, UserPermissionCategory
from log_app.serializers.user_group import *
from log_app.permissions.user_group_log_permissions import GroupHistoryPermission, PermissionHistoryPermission, PermissionCategoryHistoryPermission

class FilterForCustomGroupHistory(FilterSet):
    date = DateFromToRangeFilter(field_name='history_date', label='History date ad')
    class Meta:
        model = UserGroup.history.model
        fields = ['id','history_type','history_date_bs']

class CustomGroupHistoryViewset(viewsets.ReadOnlyModelViewSet):
    permission_classes = [GroupHistoryPermission]
    queryset = UserGroup.history.all()
    serializer_class = CustomGroupHistorySerializer
    http_method_names = ['get', 'option', 'head']
    filter_class = FilterForCustomGroupHistory
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['id','history_date']
    search_fields = ['id','history_date']


class FilterForCustomPermissionHistory(FilterSet):
    date = DateFromToRangeFilter(field_name='history_date', label='History date ad')
    class Meta:
        model = UserPermission.history.model
        fields = ['id','history_type','history_date_bs']

class CustomPermissionHistoryViewset(viewsets.ReadOnlyModelViewSet):
    permission_classes = [PermissionHistoryPermission]
    queryset = UserPermission.history.all()
    serializer_class = CustomPermissionHistorySerializer
    http_method_names = ['get', 'option', 'head']
    filter_class = FilterForCustomPermissionHistory
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['id','history_date']
    search_fields = ['id','history_date']


class FilterForPermissionCategoryHistory(FilterSet):
    date = DateFromToRangeFilter(field_name='history_date', label='History date ad')
    class Meta:
        model = UserPermissionCategory.history.model
        fields = ['id','history_type','history_date_bs']

class PermissionCategoryHistoryViewset(viewsets.ReadOnlyModelViewSet):
    permission_classes = [PermissionCategoryHistoryPermission]
    queryset =  UserPermissionCategory.history.all()
    serializer_class = PermissionCategoryHistorySerializer
    http_method_names = ['get', 'option', 'head']
    filter_class = FilterForPermissionCategoryHistory
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['id','history_date']
    search_fields = ['id','history_date']
    