from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend, DateFromToRangeFilter
from django_filters.rest_framework import FilterSet
from .sale_unique_id_generator import generate_sale_no

# imported serializers
from .serializers import SaveSaleSerializer , ListSaleDetailSerializer , ListSaleMainSerializer, SaveSaleForReturnSerializer, SalePaymentDetailSerializer,  SaleDetailForSaleReturnSerializer
from .models import SaleMain, SaleDetail, SalePaymentDetail
from rest_framework.decorators import action
from django.db import transaction
from src.item.models import Item
from src.item.serializers import GetItemSerializer
from src.custom_lib.functions import stock
from decimal import Decimal
from django.db import transaction
from .sale_permissions import SaleDetailPermission, SaveSalePermission, SaleMainPermission, SaleReturnPermission, SaleViewPermission
from django.db.models import Prefetch
from .update_purchase_order_direct_sale import update_purchase_order_direct_sale,  update_purchase_order_sale_return


class FilterForSaleMain(FilterSet):
    '''
    custom filter for sale main
    '''
    date = DateFromToRangeFilter(field_name="created_date_ad")
    class Meta:
        model = SaleMain
        fields = ['sale_no', 'customer', 'sale_details']

    def filter_queryset(self, queryset):
        sale_details = self.form.cleaned_data.get('sale_details')

        if sale_details:
            sale_details_qs = SaleDetail.objects.all()
            queryset = queryset.prefetch_related(None)
            sale_detail_ids = list(map(lambda x:x.id, sale_details))
            sale_details_qs = sale_details_qs.filter(id__in=sale_detail_ids)
            queryset = queryset.prefetch_related(Prefetch('sale_details', sale_details_qs))
        
        return super().filter_queryset(queryset)

  
class ListSaleMainViewSet(viewsets.ModelViewSet):
    '''
    model viewset  for sale main lists
    '''  
    permission_classes = [SaleMainPermission]
    queryset = SaleMain.objects.filter(sale_type =1).prefetch_related('sale_details')
    serializer_class =  ListSaleMainSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filter_class = FilterForSaleMain
    search_fields = ['sale_no', 'customer__first_name', 'customer__last_name']
    ordering_fields = ['id', 'sale_no']
    http_method_names = ['get', ]



class FilterForSaleDetail(FilterSet):
    '''
    custom filter for sale detail
    '''
    date = DateFromToRangeFilter(field_name="created_date_ad")
  
    class Meta:
        model = SaleDetail
        fields = ['item', 'sale_main']

class ListSaleDetailViewSet(viewsets.ModelViewSet):
    '''
    model viewset for sale detail lists
    '''
    permission_classes = [SaleDetailPermission]
    queryset = SaleDetail.objects.all().select_related('item','item_unit','ref_purchase_detail','ref_customer_order_detail')
    serializer_class =  ListSaleDetailSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filter_class = FilterForSaleDetail
    search_fields = ['item', 'qty']
    ordering_fields = ['id', 'item']
    http_method_names = ['get',]



class FilterForSaveSale(FilterSet):
    '''
    custom filter for save sale 
    '''
    date = DateFromToRangeFilter(field_name="created_date_ad")
    class Meta:
        model = SaleMain
        fields = ['sale_type','sale_no','customer']

class SaveSaleViewSet(viewsets.ModelViewSet):
    '''
    model viewset for save sale
    '''
    permission_classes = [SaveSalePermission]
    queryset = SaleMain.objects.all().select_related("customer", "ref_customer_order_main")
    serializer_class =  SaveSaleSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    http_method_names = ['get', 'post', 'patch']
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filter_class = FilterForSaveSale
    ordering_fields = ['id',]
    search_fields = ['sale_no','customer__first_name','customer__last_name']


    @action(url_path="get-data", detail=False)
    def get_data(self, request):
            data = {}
            items = Item.objects.filter(active=True)
            item_serializer = GetItemSerializer(items, many=True, context={"request": request})
            data['items'] = item_serializer.data
            return Response(data, status=status.HTTP_200_OK)


    @transaction.atomic
    def create(self, request, *args, **kwargs):
        '''
        create method of save sale
        '''
        request.data["sale_no"] = generate_sale_no(1)
        request.data["sale_type"] = 1

        serializer = SaveSaleSerializer(data=request.data, context={"request": request})    
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            try:
              update_purchase_order_direct_sale(serializer.data, request,supplier_priority=1)
            except Exception as e:
                raise e
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def retrieve(self, request, *args, **kwargs):
        '''
        retrieve method for save sale
        '''
        return Response({"method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class FilterForReturnSale(FilterSet):
    '''
    custom filter of return sale 
    '''
    date = DateFromToRangeFilter(field_name="created_date_ad")
    class Meta:
        model = SaleMain
        fields = ['sale_type','sale_no','customer']

class ReturnSaleView(viewsets.ModelViewSet):
    permission_classes = [SaleReturnPermission]
    queryset = SaleMain.objects.filter(sale_type=2).select_related("customer","ref_customer_order_main")
    serializer_class = SaveSaleForReturnSerializer
    http_method_names = ['post', 'head', 'get']
    filter_class =   FilterForReturnSale
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    ordering_fields = ['id', ]
    search_fields = ['id', 'sale_details__item__brand_name']



    @transaction.atomic
    def create(self, request, *args, **kwargs):

        try:
            sale_details = request.data["sale_details"]
        except KeyError:
            return Response({"key_error": "Provide sale_details"}, status=status.HTTP_400_BAD_REQUEST)
        for sale in sale_details:
            ref_id_sale = int(sale["ref_sale_detail"])
            total_quantity = SaleDetail.objects.values_list(
                "qty", flat=True).get(pk=ref_id_sale)
            return_quantity = sum(SaleDetail.objects.filter(ref_sale_detail=ref_id_sale)
                                  .values_list("qty", flat=True)) + Decimal(sale["qty"])

            if total_quantity < return_quantity:
                return Response("Return items ({}) more than sale items({})".format(return_quantity, total_quantity),
                                status=status.HTTP_400_BAD_REQUEST)


        request.data["sale_no"] = generate_sale_no(2)
        request.data["sale_type"] = 2
        serializer = SaveSaleForReturnSerializer(
            data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            try:
              update_purchase_order_sale_return(serializer.data)
            except Exception as e:
                raise e
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, *args, **kwargs):
        return Response({"method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



class SalePaymentDetailView(viewsets.ReadOnlyModelViewSet):
    queryset = SalePaymentDetail.objects.all().select_related("sale_main","payment_mode")
    serializer_class = SalePaymentDetailSerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ["sale_main__customer_first_name"]
    filter_fields = ["sale_main", "id", "payment_mode"]
    ordering_fields = ["id"]



class SaleDetailForReturnViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [SaleViewPermission]
    queryset = SaleDetail.objects.filter(ref_sale_detail__isnull=True)
    serializer_class = SaleDetailForSaleReturnSerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ["item__brand_name", "customer__first_name"]
    filter_fields = ["sale_main", "item"]
    ordering_fields = ["id", "sale_main"]