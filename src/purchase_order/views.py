
from random import choices
from rest_framework.viewsets import  ReadOnlyModelViewSet
from .models import PurchaseOrderDetail, PurchaseOrderMain, PurchaseOrderReceivedDetail, PurchaseOrderReceivedMain
from .serializers import ListPurchaseOrderMainSerializer, ListPurchaseOrderReceivedMainSerializer, SavePurchaseOrderReceivedMainSerializer
from .serializers import SavePurchaseOrderMainSerializer,  UpdatePurchaseOrderMainSerializer, DeletePurchaseOrderReceivedDetailSerializer

from django_filters.rest_framework import DjangoFilterBackend, DateFromToRangeFilter
from rest_framework.filters import OrderingFilter, SearchFilter
import django_filters
from django_filters.rest_framework import FilterSet
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import transaction
from rest_framework.decorators import action
from django.db import transaction
from src.item.models import Item
from src.item.serializers import GetItemSerializer
from .purchase_order_unique_id_generator import generate_order_no, generate_purchase_order_received_no
from .purchase_order_permissions import PurchaseOrderSavePermission, PurchaseOrderReceivedPermission, \
            QuickUpdatePurchaseOrderPermission,  PurchaseOrderGetPermission, PurchaseOrderReceivedGetPermission
from rest_framework import generics
from django.db.models import Prefetch
from .update_purchase_order import  update_po_detail_delete_purchase_received



class FilterForListPurchaseOrder(django_filters.FilterSet):
    '''
    custom filter for Purchase order main listing data
    '''
    date = DateFromToRangeFilter(field_name="created_date_ad")
    informed = django_filters.BooleanFilter(field_name="purchase_order_details__informed", distinct=True)
    available = django_filters.ChoiceFilter(choices=PurchaseOrderDetail.AVAILABLE, field_name="purchase_order_details__available", distinct=True) 
    
    class Meta:
        model = PurchaseOrderMain
        fields = ['search_list', 'purchase_order_type','informed', 'available']


class ListPurchaseOrderMainViewSet(ReadOnlyModelViewSet):
    '''
    ReadOnlyModelViewSet for purchase order main listing data
    '''
    permission_classes=[PurchaseOrderGetPermission]
    queryset = PurchaseOrderMain.objects.all()
    serializer_class = ListPurchaseOrderMainSerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ['search_list' ,'id','supplier__name','purchase_order_details__item__brand_name']
    ordering_fields = ['search_list', 'id']
    filter_class =  FilterForListPurchaseOrder


class FilterForListPurchaseOrderReceived(django_filters.FilterSet):
    '''
    custom filter for Purchase order main listing data
    '''
    date = DateFromToRangeFilter(field_name="created_date_ad")
   
    class Meta:
        model = PurchaseOrderReceivedMain
        fields = ['supplier','purchase_order_received_no' , 'purchase_order_received_type']

class ListPurchaseOrderReceivedMainViewSet(ReadOnlyModelViewSet):
    '''
    ReadOnlyModelViewSet for purchase order main listing data
    '''
    permission_classes = [PurchaseOrderReceivedGetPermission]
    queryset = PurchaseOrderReceivedMain.objects.filter(purchase_order_received_details__archived= False).select_related("supplier","purchase_order_main")
    serializer_class = ListPurchaseOrderReceivedMainSerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = [ 'id', 'purchase_order_received_details__item__brand_name']
    ordering_fields = [ 'id',]
    filter_class =  FilterForListPurchaseOrderReceived


    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(purchase_order_received_details__archived=False).prefetch_related(
                Prefetch(
                    "purchase_order_received_details",
                    queryset=PurchaseOrderReceivedDetail.objects.filter(archived=False),
                ),
            ).distinct()
        return queryset



class SavePurchaseOrderView(viewsets.ModelViewSet):
    permission_classes = [PurchaseOrderSavePermission]
    queryset = PurchaseOrderMain.objects.all().select_related('assigned_to','supplier').prefetch_related('purchase_order_details')
    serializer_class = SavePurchaseOrderMainSerializer


    @action(url_path="get-data", detail=False)
    def get_data(self, request):
            data = {}
            items = Item.objects.filter(active=True)
            item_serializer = GetItemSerializer(items, many=True, context={"request": request})
            data['items'] = item_serializer.data
            return Response(data, status=status.HTTP_200_OK)


    @transaction.atomic
    def create(self, request, **kwargs):
        request.data['purchase_order_type'] = 1
        request.data['purchase_order_no'] = generate_order_no(1)

        serializer = SavePurchaseOrderMainSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        return Response({"method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



class FilterForReceivedPurchaseOrder(FilterSet):
    '''
    custom filter of  receive purchase order
    '''
    date = DateFromToRangeFilter(field_name="created_date_ad")
    class Meta:
        model = PurchaseOrderReceivedMain
        fields = ['purchase_order_received_type', 'purchase_order_received_no','supplier']


class PurchaseOrderReceivedView(viewsets.ModelViewSet):
    '''
    model viewset for receive purchase order
    '''
    permission_classes = [PurchaseOrderReceivedPermission]
    http_method_names = ['get', 'head', 'post']
    serializer_class =  SavePurchaseOrderReceivedMainSerializer
    queryset = PurchaseOrderReceivedMain.objects.all().select_related('supplier','purchase_order_main').prefetch_related('purchase_order_received_details')
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filter_class = FilterForReceivedPurchaseOrder
    ordering_fields = ['id',]
    search_fields = ['purchase_order_received_no', 'purchase_order_received_details__item__brand_name']


    @transaction.atomic
    def create(self, request, *args, **kwargs):
        '''
        create method for purchase order receive
        '''

        try:
            request.data['purchase_order_main']
            
        except KeyError:
            return Response('Provide purchase_order_main key',
                            status=status.HTTP_400_BAD_REQUEST)  
        try:
            request.data['supplier']
        except KeyError:
            return Response('Provide supplier key', status=status.HTTP_400_BAD_REQUEST)

        purchase_order_main_id = request.data['purchase_order_main']
        if PurchaseOrderReceivedMain.objects.filter(purchase_order_main= purchase_order_main_id ).exists():
            return Response('Order already Received or pending', status=status.HTTP_400_BAD_REQUEST)


        request.data['purchase_order_received_no'] = generate_purchase_order_received_no(1)
        request.data['purchase_order_received_type'] = 1
         

        serializer =  SavePurchaseOrderReceivedMainSerializer(data=request.data,
                                                                      context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuickUpdatePurchaseOrderMainViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [QuickUpdatePurchaseOrderPermission]
    serializer_class =  UpdatePurchaseOrderMainSerializer
    queryset = PurchaseOrderMain.objects.all()
    http_method_names = ['patch',]

    @transaction.atomic
    @action(detail= True, url_path="quick-update", methods=['PATCH'])
    def patch(self, request, pk):
        instance = PurchaseOrderMain.objects.get(id=pk)
        serializer =  UpdatePurchaseOrderMainSerializer(instance , data = request.data, partial=True, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class DeletePurchaseOrderReceivedViewSet(generics.DestroyAPIView):
  
    queryset = PurchaseOrderReceivedDetail.objects.all()

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        '''
        Delete method of purchase order received
        '''
        instance = self.get_object()
        instance.archived=True
        net_amount_detail= instance.net_amount
        purchase_received_main_total_amount_org= instance.purchase_order_received_main.total_amount
        #get purchase order received main data to update total amount after deleted purchase order received detail
        purchase_order_received_main_data= PurchaseOrderReceivedMain.objects.get(
            id= instance.purchase_order_received_main.id)
        purchase_order_received_main_data.total_amount =  (purchase_received_main_total_amount_org-net_amount_detail)
        purchase_order_received_main_data.save()
        instance.save()
        queryset = PurchaseOrderReceivedDetail.objects.filter(purchase_order_received_main=instance.purchase_order_received_main.id, archived=False)
        serializer = DeletePurchaseOrderReceivedDetailSerializer(queryset, many=True)  
        update_po_detail_delete_purchase_received(instance.id, serializer.data, supplier_priority=1)
        return Response(serializer.data, status=status.HTTP_200_OK)    

   
