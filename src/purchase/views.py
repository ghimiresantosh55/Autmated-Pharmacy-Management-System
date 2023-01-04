
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend, DateFromToRangeFilter
from django_filters.rest_framework import FilterSet
import django_filters
from src.purchase_order.models import PurchaseOrderReceivedMain
from src.customer_order.models import OrderMain, OrderDetail
from src.purchase_order.serializers import SavePurchaseOrderReceivedMainSerializer
from .serializers import  ListPurchaseMainSerializer,  ListPurchaseDetailSerializer, SaveOpeningStockSerializer, \
    SavePurchaseMainSerializer, SavePurchaseMainForReturnSerializer, UpdatePurchaseDetailSerializer,  DirectpurchaseSerializer
from src.custom_lib.serializers.stock_serializers import PurchaseDetailStockSerializer
from rest_framework.decorators import action
import decimal
from decimal import Decimal
from src.item.models import Item
from src.item.serializers import GetItemSerializer
from .models import PurchaseMain, PurchaseDetail
from .purchase_permissions import PurchaseDetailPermission,  PurchaseMainPermission, OpeningStockPermission,\
     PurchaseOrderVerifiedPermission, PurchaseReturnPermission, UpdatePurchaseDetailPermission,  DirectPurchasePermission
from src.custom_lib.functions import stock
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import transaction
from src.purchase_order.purchase_order_unique_id_generator import  generate_purchase_order_received_no
from  .purchase_unique_id_generator import generate_purchase_no
from . update_purchase_order_direct_purchase import update_purchase_order_direct_purchase, update_purchase_order_save_opening_stock
from . update_purchase_order_purchase_return import update_purchase_order_purchase_return
from . update_purchase_order_purchase_entry_edit import update_po_detail_edit_purchase_entry


# Create your views here.
class FilterForPurchaseMain(FilterSet):
    '''
    custom filter for purchase main
    '''
    date = DateFromToRangeFilter(field_name="created_date_ad")
    class Meta:
        model = PurchaseMain
        fields = ['purchase_no', 'supplier__name','supplier']
  
class ListPurchaseMainViewSet(viewsets.ModelViewSet):
    '''
    model viewset of listing purchase main data
    '''
    permission_classes = [PurchaseMainPermission]
    queryset = PurchaseMain.objects.filter(purchase_type =1).select_related('supplier')
    serializer_class =   ListPurchaseMainSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filter_class = FilterForPurchaseMain
    search_fields = ['purchase_no', 'supplier__name']
    ordering_fields = ['id', 'purchase_no']
    http_method_names = ['get', ]


class FilterForPurchaseDetail(FilterSet):
    '''
    custom filter of purchase detail
    '''
    date = DateFromToRangeFilter(field_name="created_date_ad")
    class Meta:
        model = PurchaseDetail
        fields = ['item__brand_name', 'qty', 'amount', 'location']
  

class ListPurchaseDetailViewSet(viewsets.ModelViewSet):
    '''
    model viewset for listing purchase detail data
    '''
    permission_classes = [PurchaseDetailPermission]
    queryset = PurchaseDetail.objects.all().select_related('purchase_main','item','item_unit','ref_purchase_order_received_detail','location')
    serializer_class =  ListPurchaseDetailSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filter_class = FilterForPurchaseDetail
    search_fields = ['item__brand_name', 'qty', 'amount', 'location__name' ]
    ordering_fields = ['id', 'qty']
    http_method_names = ['get', ]


class FilterForVerifyPurchaseOrder(FilterSet):
    '''
    custom filter of verify purchase order
    '''
    date = DateFromToRangeFilter(field_name="created_date_ad")
    class Meta:
        model = PurchaseMain
        fields = ['purchase_type','purchase_no','supplier']


class VerifyPurchaseOrderView(viewsets.ModelViewSet):
    '''
    model viewset for verify purchase order 
    '''
    permission_classes = [PurchaseOrderVerifiedPermission]
    http_method_names = ['get', 'head', 'post',]
    serializer_class = SavePurchaseMainSerializer
    queryset = PurchaseMain.objects.all().select_related("supplier", "ref_purchase_order_received_main").prefetch_related('purchase_details')
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filter_class = FilterForVerifyPurchaseOrder
    ordering_fields = ['id',]
    search_fields = ['purchase_no', 'purchase_details__item__brand_name']


    @action(url_path="get-data", detail=False)
    def get_data(self, request):
        '''
        get data for item
        '''
        data = {}
        items = Item.objects.filter(active=True)
        item_serializer = GetItemSerializer(items, many=True, context={"request": request})
        data['items'] = item_serializer.data
        return Response(data, status=status.HTTP_200_OK)


    @transaction.atomic
    def create(self, request, *args, **kwargs):
        '''
        create method for verify purchase order
        ''' 
        # print(request.data, "request data")        
        try:
            purchase_order_received_main = request.data.pop('purchase_order_received_main')
        except KeyError:
            return Response('Provide purchase Order received Data in purchase_order_received_main key',
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            ref_purchase_order_received_main = purchase_order_received_main['ref_purchase_order_received_main']
            
        except KeyError:
            return Response('Provide ref_purchase_order_received_main key in purchase_order_received_main key',
                            status=status.HTTP_400_BAD_REQUEST)  

        try:
            purchase_main = request.data.pop('purchase_main')
        except KeyError:
            return Response('Provide purchase Data in purchase_main key')

        try:
            purchase_main['ref_purchase_order_received_main']

        except KeyError:
            return Response('Provide ref_purchase_order_received_main key', status=status.HTTP_400_BAD_REQUEST)

        try:
            purchase_main['supplier']
        except KeyError:
            return Response('Provide supplier key', status=status.HTTP_400_BAD_REQUEST)

        
        purchase_order_received_main_ref_id = purchase_order_received_main['ref_purchase_order_received_main']
        if PurchaseOrderReceivedMain.objects.filter(ref_purchase_order_received_main = purchase_order_received_main_ref_id).exists():
            return Response('Received Purchase Order already Verified or Cancelled', status=status.HTTP_400_BAD_REQUEST)
      
        purchase_order_receive_main_data =  PurchaseOrderReceivedMain.objects.get(id = purchase_order_received_main_ref_id)
     
        if purchase_order_receive_main_data.purchase_order_received_type ==2:
            return Response('Invalid Purchase order received', status=status.HTTP_400_BAD_REQUEST)

        
        purchase_order_received_serializer = SavePurchaseOrderReceivedMainSerializer(data=purchase_order_received_main, 
                                                                context={'request': request})     

        #insert data for purchase main
        purchase_main['purchase_no'] = generate_purchase_no(1)
        purchase_main['purchase_type'] = 1

       
        updated_purchase_details = purchase_main['purchase_details']
        # update price fields in purchase
        for detail in updated_purchase_details:
            if  detail['item_price']!=""or  not None:
                detail['price'] = detail['item_price']

        # update price(mrp) field of item from purchase entry
        item_data = Item.objects.get(id = detail['item'])
        item_data.price =   detail['price']
        item_data.save()

      
        customer_order_data= OrderDetail.objects.filter(item = detail['item'])
        decimal.getcontext().rounding=decimal.ROUND_HALF_UP
        quantize_places = Decimal(10) ** -2
      
        for co_order in customer_order_data:
            co_order.amount = detail['price']
            n_amount = co_order.net_amount
            co_order.sub_total= Decimal(co_order.amount*co_order.qty)
            co_order.sub_total.quantize(quantize_places)
            co_order.discount_amount=  Decimal(co_order.sub_total*co_order.discount_rate/100)
            co_order.discount_amount.quantize(quantize_places)
            co_order.net_amount=Decimal(co_order.sub_total-co_order.discount_amount)
            co_order.net_amount.quantize(quantize_places)
            co_order.save()
            
            co_main_data= OrderMain.objects.filter(total_amount = co_order.order.total_amount)
            for co_data in co_main_data:
                t_amount =  co_data.total_amount - n_amount
                print(t_amount, "this is t amount")
                co_data.total_amount = t_amount + co_order.net_amount
                co_data.total_amount.quantize(quantize_places)
                print(co_data.total_amount)
                co_data.save() 
        
        purchase_main['purchase_details'] = updated_purchase_details 

        purchase_serializer = SavePurchaseMainSerializer(data= purchase_main, context={'request': request})

        #insert data for purchase order received  main
        purchase_order_received_main['purchase_order_received_no'] = generate_purchase_order_received_no(2)
        purchase_order_received_main['purchase_order_received_type'] = 2

        #saving both fields data
        if purchase_serializer.is_valid(raise_exception=True):
            if purchase_order_received_serializer.is_valid(raise_exception=True):
                    purchase_serializer.save()
                    purchase_order_received_serializer.save()
                
                    try:
                        update_po_detail_edit_purchase_entry(
                            purchase_order_received_data = purchase_order_received_serializer.data, 
                            purchase_data = purchase_serializer.data, request= request, supplier_priority=1
                            )
                    
                    except Exception as e:
                        raise e
                
                    return Response(purchase_order_received_serializer.data, status=status.HTTP_201_CREATED)
            else:
                    return Response(purchase_order_received_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(purchase_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class FilterForSaveOpeningStock(FilterSet):
    '''
    custom filter for save opening stock
    '''
    date = DateFromToRangeFilter(field_name="created_date_ad")
    class Meta:
        model = PurchaseMain
        fields = ['purchase_type','purchase_no','supplier']


class SaveOpeningStockViewset(viewsets.ModelViewSet):
    '''
    model viewset for save opening stock
    '''
    permission_classes = [OpeningStockPermission]
    queryset = PurchaseMain.objects.filter(purchase_type=3).select_related('supplier').prefetch_related('purchase_details')
    serializer_class = SaveOpeningStockSerializer
    http_method_names = ['get', 'list', 'head','post']
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filter_class = FilterForSaveOpeningStock
    ordering_fields = ['id',]
    search_fields = ['purchase_no']


    @action(url_path="get-data", detail=False)
    def get_data(self, request):
        '''
        method for get data 
        '''
        data = {}
        items = Item.objects.filter(active=True)
        item_serializer = GetItemSerializer(items, many=True, context={"request": request})
        data['items'] = item_serializer.data
        return Response(data, status=status.HTTP_200_OK)

    

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        '''
        create method for save opening stock
        '''
        request.data['purchase_no'] = generate_purchase_no(3)
        request.data['purchase_type'] = 3

        serializer = SaveOpeningStockSerializer(data=request.data, context={'request': request})

        if not serializer.is_valid(raise_exception=True):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        try:
               update_purchase_order_save_opening_stock(serializer.data)
        except Exception as e:
                raise e
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class FilterForPurchaseDetailStock(django_filters.FilterSet):
    '''
    custom filter for purchase detail stock
    '''
    date = django_filters.DateFromToRangeFilter(field_name="created_date_ad")  
    class Meta:
        model = PurchaseDetail
        fields = ['id', 'purchase_main', 'purchase_main__supplier', 'item']


class PurchaseDetailStockViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    model viewset for purchase detail stock
    '''
    queryset = PurchaseDetail.objects.filter(ref_purchase_detail__isnull=True).select_related('purchase_main','item','item_unit','ref_purchase_order_received_detail','location')
    serializer_class = PurchaseDetailStockSerializer
    filter_class = FilterForPurchaseDetailStock 
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    ordering_fields = ['id',  'item__brand_name']
    search_fields = ['item__name','item__code']



class FilterForReturnPurchase(FilterSet):
    '''
    custom filter of return purchase 
    '''
    date = DateFromToRangeFilter(field_name="created_date_ad")
    class Meta:
        model = PurchaseMain
        fields = ['purchase_type','purchase_no','supplier']


class ReturnPurchaseView(viewsets.ModelViewSet):
    '''
    model viewset for Return Purchase
    '''
    permission_classes = [PurchaseReturnPermission]
    serializer_class =  SavePurchaseMainForReturnSerializer
    http_method_names = ['post', 'head', 'get']
    queryset = PurchaseMain.objects.all().filter(purchase_type=2).select_related("supplier", "ref_purchase_order_received_main").prefetch_related('purchase_details')
    filter_class =  FilterForReturnPurchase
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    ordering_fields = ['id', ]
    search_fields = ['id', 'purchase_details__item__brand_name']


    @transaction.atomic
    def create(self, request, *args, **kwargs):
        purchase_detail = request.data['purchase_details']

        for detail in purchase_detail:
            ref_purchase_detail = int(detail['ref_purchase_detail'])
            remaining_quantity = stock.get_remaining_qty_of_purchase(ref_purchase_detail)
            qty = Decimal(detail['qty'])
            if remaining_quantity < qty:
                return Response("Invalid return qty for item {} :remaining quantity {}".format(detail['item'],
                                                                                               remaining_quantity),
                                status=status.HTTP_403_FORBIDDEN)

        request.data['purchase_no'] = generate_purchase_no(2)
        request.data['purchase_type'] = 2
        serializer = SavePurchaseMainForReturnSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid(raise_exception=True):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        try:
               update_purchase_order_purchase_return(serializer.data, request, supplier_priority=1)
        except Exception as e:
                raise e
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def retrieve(self, request, *args, **kwargs):
        return Response({"method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class UpdatePurchaseDetailViewSet(viewsets.ModelViewSet):
    permission_classes = [UpdatePurchaseDetailPermission]
    serializer_class =  UpdatePurchaseDetailSerializer
    queryset = PurchaseDetail.objects.all().select_related('purchase_main','item','item_unit','ref_purchase_order_received_detail','location')
    http_method_names = ['patch',]

  
    def patch(self, request, pk):
        instance = PurchaseDetail.objects.get(id=pk)
        serializer =   UpdatePurchaseDetailSerializer(instance , data = request.data, partial=True, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FilterForDirectPurchase(FilterSet):
   
    date = DateFromToRangeFilter(field_name="created_date_ad")
    class Meta:
        model = PurchaseMain
        fields = ['purchase_type','purchase_no','supplier']

class DirectPurchaseView(viewsets.ModelViewSet):
    permission_classes = [DirectPurchasePermission]
    http_method_names = ['get', 'head', 'post',]
    serializer_class =  DirectpurchaseSerializer
    queryset = PurchaseMain.objects.all().select_related("supplier", "ref_purchase_order_received_main").prefetch_related('purchase_details')
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filter_class =FilterForDirectPurchase
    ordering_fields = ['id',]
    search_fields = ['purchase_no', 'purchase_details__item__brand_name']


    @transaction.atomic
    def create(self, request, *args, **kwargs):
       
        request.data["purchase_no"] = generate_purchase_no(1)
        request.data["purchase_type"] = 1
        
        serializer = DirectpurchaseSerializer(
            data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            try:
               update_purchase_order_direct_purchase(serializer.data)
            except Exception as e:
                raise e
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)