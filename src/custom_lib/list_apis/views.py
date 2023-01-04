from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend, DateFromToRangeFilter
from django_filters.rest_framework import FilterSet
import django_filters
from.serializers import ItemListSerializer
from src.item.models import Item
from src.core_app.pagination import CustomPagination


class FilterForItemList(FilterSet):
    date = DateFromToRangeFilter(field_name="created_date_ad")
    class Meta:
        model = Item
        fields = ['id','brand_name',]


class ItemListView(ListAPIView):
    queryset = Item.objects.filter(active=True)
    serializer_class = ItemListSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    filter_class = FilterForItemList
    search_fields = ['brand_name']
    ordering_fields = ['id', ]
    pagination_class = CustomPagination