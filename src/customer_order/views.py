
from random import choices
from requests import request
from rest_framework import viewsets
from django.db import transaction
# filter
from django_filters.rest_framework import DjangoFilterBackend,  DateFromToRangeFilter
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework import status
from .order_id_generator import generate_customer_order_no
from django.db.models import Prefetch
from django.core.exceptions import ValidationError
from src.user.models import User

# importing Models needed in below classes
# from src.item.models import Item
import django_filters
from django_filters.rest_framework import FilterSet
import django_filters
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from src.item.models import Item
from src.item.serializers import GetItemSerializer
from .models import OrderMain, OrderDetail
from .purchase_order_create import create_purchase_order, update_po_co_canceld, update_po_detail_co_canceld
import traceback
from django.core.paginator import Paginator
from rest_framework import generics
from simple_history.utils import update_change_reason
# from src.item.models import Item
from . serializers import CustomerOrderDispatchCreateSerializer,  OrderDetailSerializer, SaveCustomerOrderSerializer, UpdateOrderMainSerializer, CustomerOrderDispatchViewSerializer,\
        DeleteOrderDetailSerializer, SaveOrderDetailSerializer, BulkUpdateOrderMainSerializer, AmountStatusBulkUpdateSerializer
# permissions
from .customer_order_permissions import  SavecustomerOrderPermission, OrderDetailPermission, customerOrderPermission, customerOrderDispatchPermission
from rest_framework.views import APIView, Response
from django_filters import rest_framework as filters
from src.credit_management.models import CreditClearance



class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass


class RangeFilterForOrderMain(filters.FilterSet):
    date = DateFromToRangeFilter(field_name="created_date_ad")
    informed = django_filters.BooleanFilter(field_name="order_details__informed") 
    # delivery_status= django_filters.ModelMultipleChoiceFilter(choices="DELIVERY_STATUS_TYPE",queryset=OrderMain.objects.all(), conjoined=True)
    delivery_status_in = NumberInFilter(field_name='delivery_status', lookup_expr='in')
  
    
  
    class Meta:
        model = OrderMain
        fields = ['customer__first_name','customer__last_name', 'customer__phone_no', 'delivery_person', 'delivery_status_in','order_no','amount_status', 'order_location', 'informed']

    
class SaveOrderMainViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [SavecustomerOrderPermission]   
    queryset = OrderMain.objects.filter(order_details__archived=False).select_related("delivery_person","customer")
    serializer_class = SaveCustomerOrderSerializer
    filter_class = RangeFilterForOrderMain
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['id',]
    search_fields = ['customer__first_name','customer__last_name','customer__phone_no','order_no','amount_status','order_location','order_details__item__brand_name']
    http_method_names = ['get', 'post', 'patch']
   
      
    def get_queryset(self):
        queryset = super().get_queryset()
        user= self.request.user
        queryset = queryset.filter(order_details__archived=False).prefetch_related(
                Prefetch(
                    "order_details",
                    queryset=OrderDetail.objects.filter(archived=False),
                ),
            ).distinct()
        return queryset if user.is_superuser else queryset.filter(created_by=user)

    @action(url_path="get-data", detail=False)
    def get_data(self, request):
            data = {}
            items = Item.objects.filter(active=True)
            item_serializer = GetItemSerializer(items, many=True)
            data['items'] = item_serializer.data
            return Response(data, status=status.HTTP_200_OK)


    @transaction.atomic
    def create(self, request, *args, **kwargs):  
        request.data['order_no'] = generate_customer_order_no()
        order_serializers =  SaveCustomerOrderSerializer(data= request.data, context={'request': request})
      
        if order_serializers.is_valid(raise_exception = True):
            order_serializers.save()
            """
            Create purchase order on customer order save
            """
            try:
                create_purchase_order(order_serializers.data, request, supplier_priority=1)
            except Exception as e:
                raise e

            # --------------------------------------------------
            return Response(order_serializers.data, status=status.HTTP_201_CREATED)
        return Response(order_serializers.errors, status=status.HTTP_400_BAD_REQUEST)


    
    @transaction.atomic
    def partial_update(self, request, pk, *args, **kwargs):
        order_instance = OrderMain.objects.get(id=pk)
      
        try:
            remarks = str(request.data['remarks']).strip()
            if len(remarks) <= 0:
                return Response({'remarks': 'Please give at least one word for remarks'},
                                status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'remarks': 'Please Provide remarks'}, status=status.HTTP_400_BAD_REQUEST)
        
        """************ data filtering for order details*********************************"""
        order_details_update_data = list()
        order_details_create_data = list()
        order_details_data =  request.data.pop('order_details')

        for order_detail_data in order_details_data:

            if "id" in  order_detail_data:
                  order_details_update_data.append(order_detail_data)
            else: 
                order_details_create_data.append(order_detail_data)

        """******************************update order details*********************************"""
        for order_detail_update_data in  order_details_update_data:
            order_detail_instance = OrderDetail.objects.get(id=int(order_detail_update_data['id']))
        
            order_detail_update_serializer = OrderDetailSerializer(order_detail_instance, data=order_detail_update_data, partial=True, context={"request":request})
            if   order_detail_update_serializer.is_valid():
                  order_detail_update_serializer.save()
                
            else:
                return Response(order_detail_update_serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
        """******************************create order details*********************************"""
        order_details_for_po = []
        for order_detail_create_data in order_details_create_data:
            order_detail_create_data['order'] = order_instance.id
            order_detail_create_serializer = OrderDetailSerializer(data= order_detail_create_data,  context={"request":request})
           
            if  order_detail_create_serializer.is_valid(raise_exception=True):
                order_detail_create_serializer.save()
                order_details_for_po.append(order_detail_create_serializer.data)
                order_detail_instance = OrderDetail.objects.get(id=int(order_detail_create_serializer.data['id']))
            else:
                return Response(order_detail_create_serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        
        #  raising PO for created customer orders
        create_purchase_order({"order_details": order_details_for_po }, self.request, 1)
        
        order_main_serializer = SaveCustomerOrderSerializer(order_instance, data = request.data, partial=True)
        if order_main_serializer.is_valid(raise_exception=True):
            order_main_serializer.save()
            update_change_reason(order_instance, remarks)

            queryset = OrderMain.objects.filter(order_details__archived=False).prefetch_related(
                    Prefetch(
                        "order_details",
                        queryset=OrderDetail.objects.filter(archived=False),
                        ),).distinct().get(id = order_instance.id)
            
            order_main_serializer = SaveCustomerOrderSerializer(queryset)
            return Response(order_main_serializer.data, status= status.HTTP_200_OK)
        return Response(order_main_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            



class OrderMainViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [customerOrderPermission]
    serializer_class =  UpdateOrderMainSerializer
    queryset = OrderMain.objects.all()
    http_method_names = ['patch',]

    @transaction.atomic
    @action(detail= True, url_path = "quick-update", methods=['PATCH'])
    def patch(self, request, pk):
        instance = OrderMain.objects.get(id=pk)

        if  request.data['delivery_status']==2:
            serializer = UpdateOrderMainSerializer(instance, data = request.data, partial=True, context={'request': request,  'pk': pk})
            
            if serializer.is_valid(raise_exception=True):
                serializer.save()  
                update_po_co_canceld(pk)   
                return Response([], status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = UpdateOrderMainSerializer(instance , data = request.data, partial=True, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 

class  OrderMainBulkUpdate(APIView):
    serializer_class =  BulkUpdateOrderMainSerializer
    
    @transaction.atomic
    def put(self,request, *args, **kwargs):
        data = request.data
        id_list = data['order_id_list']
        instances = []
        for temp in id_list:
            order = OrderMain.objects.get(id=temp)
            order.acknowledge_order=data['acknowledge_order']
            delivery_person_db = User.objects.get(id=data['delivery_person'])
            order.delivery_person =  delivery_person_db
            order.delivery_status= data['delivery_status']
            if  order.delivery_status==2:
                order_details = OrderDetail.objects.filter(order= order)
                for order_detail in order_details:
                    order_detail.cancelled=True
                    order_detail.save()
            order.save()       
            instances.append(order)
        if  request.data['delivery_status']==2:
            serializer = BulkUpdateOrderMainSerializer(instances) 
            return Response([], status=status.HTTP_200_OK)
   
        serializer = BulkUpdateOrderMainSerializer(instances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
            
     
            
class FilterForOrderDetail(FilterSet):
    '''
    custom filter for medicine form
    '''
    date = DateFromToRangeFilter(field_name="created_date_ad")
    class Meta:
        model = OrderDetail
        fields = ['id', 'item','qty','informed','amount']
      
        
class OrderDetailViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [OrderDetailPermission]
    queryset = OrderDetail.objects.filter(archived=False)
    serializer_class = SaveOrderDetailSerializer
    filter_class = FilterForOrderDetail
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ['id', 'item','qty']
    ordering_fields = ['id', 'item']
    http_method_names = ['get', 'head', 'delete']


   
class DeleteCustomerOrderViewSet(generics.DestroyAPIView):
    '''
    Delete APIview for customer order
    '''
    queryset = OrderDetail.objects.all()

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.archived=True
        instance.cancelled= True
        instance.save()

        order_main=OrderMain.objects.get(id=instance.order.id)
        print(order_main, "this is order main")
        net_amount=instance.net_amount
        order_total_amount= order_main.total_amount
        print(order_total_amount, "this is order total amount")
        order_main.total_amount= order_total_amount-net_amount
        print(order_main.total_amount, " this is after calculation")
        order_main.save()
        
        queryset = OrderDetail.objects.filter(order=instance.order.id, archived=False)
        serializer = DeleteOrderDetailSerializer(queryset, many=True)
        update_po_detail_co_canceld(instance.id)
        return Response(serializer.data, status=status.HTTP_200_OK)



# class DeleteCustomerOrderCancelled(generics.DestroyAPIView):
#     queryset = OrderMain.objects.all()

#     @transaction.atomic
#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
#         if instance.delivery_status==2:


class FilterForCustomerOrderDispatch(FilterSet):  
    date = DateFromToRangeFilter(field_name="created_date_ad")
    class Meta:
        model = OrderMain
        fields = ['delivery_person','order_no','customer', 'delivery_status']


class CustomerOrderMainDispatchViewSet(viewsets.ModelViewSet):
    permission_classes = [customerOrderDispatchPermission]
    queryset =  OrderMain.objects.filter(order_details__archived=False, delivery_status__in=[5,6]).distinct()
    http_method_names = ['get','patch','head']
    filter_class = FilterForCustomerOrderDispatch
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ['id', 'order_no','customer__first_name']
    ordering_fields = ['id', ]

  
    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return CustomerOrderDispatchCreateSerializer
        else:
            return CustomerOrderDispatchViewSerializer
        

    @transaction.atomic
    def partial_update(self, request,pk,  **kwargs):
        instance = self.get_object()  
        serializer = CustomerOrderDispatchCreateSerializer(instance, data = request.data, partial=True, context={'request': request,  'pk': pk})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            # print(serializer.data, "this is serializer data")
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class AmountStatusBulkUpdate(APIView):
#     serializer_class = AmountStatusBulkUpdateSerializer
#     queryset = OrderMain.objects.all()


class AmountStatusBulkUpdate(viewsets.ModelViewSet):
    '''
    Model viewset for update bulk amount
    '''

    serializer_class = AmountStatusBulkUpdateSerializer
    queryset = OrderMain.objects.all()
    
    @transaction.atomic
    def get_object(self, obj_id):
        try:
            return OrderMain.objects.get(id=obj_id)
        except (OrderMain.DoesNotExist, ValidationError):
            raise status.HTTP_400_BAD_REQUEST


       
    def create (self, request,*args, **kwargs):
        data = request.data
        # print(data, "this is data")
        instances = []

        for temp in data['order_mains']:
            id = temp['id']
            order = self.get_object(id)
            order.amount_status = 1
            order.save()       
            instances.append(order)

        # serializer = AmountStatusBulkUpdateSerializer(instances , many= True)
        # serializer = AmountStatusBulkUpdateSerializer(data = data, context={'request': request},  many = True)
           
        # if serializer.is_valid():
        #     serializer.save()

        # return Response(serializer.data, status=status.HTTP_200_OK)
        return super().create(request, *args, **kwargs)


        