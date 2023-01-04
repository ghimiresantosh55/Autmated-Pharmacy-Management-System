'''
view for company app
'''
# third-party
from rest_framework import viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response


# # imported serializers
from .serializers import CompanySerializer
from src.item.serializers import PoPrioritySerializer
import django_filters

# imported models
from .models import Company
from src.item.models import PoPriority
from .company_permissions import CompanyPermission

# for log
from simple_history.utils import update_change_reason
from django.db import transaction
from drf_nested_forms.utils import NestedForm


class FilterForCompany(django_filters.FilterSet):
    '''
    custom filter for company
    '''
    date = django_filters.DateFromToRangeFilter(field_name="created_date_ad")
    name = django_filters.CharFilter(lookup_expr='iexact')
    address = django_filters.CharFilter(lookup_expr='iexact')
    class Meta:
        model = Company
        fields =['name', 'active']

class CompanyViewSet(viewsets.ModelViewSet):
    '''
    model viewset for company
    '''
    permission_classes = [CompanyPermission]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filter_class = FilterForCompany
    search_fields = ['name',]
    ordering_fields = ['id', 'name',]
    http_method_names = ['get', 'post', 'patch']


    @transaction.atomic
    def create(self, request, *args, **kwargs):  
        requestData = NestedForm(request.data)
        requestData.is_nested(raise_exception=True)
        request_data = requestData.data.copy()

        for po_priority in request_data['po_priorities']:
           
          
            if po_priority['supplier']==None or  po_priority['supplier']=="":
                    request_data['po_priorities'] = []
            
        company_serializers = CompanySerializer(data= request_data, context={'request': request})
       
        if company_serializers.is_valid(raise_exception = True):
            company_serializers.save()
            return Response(company_serializers.data, status=status.HTTP_201_CREATED)
        return Response(company_serializers.errors, status=status.HTTP_400_BAD_REQUEST)



    @transaction.atomic
    def partial_update(self, request, pk, *args, **kwargs):
      
        '''
        this update method will update company and po priority also create po if there is no po priority id
        '''
        requestData = NestedForm(request.data)
        requestData.is_nested(raise_exception=True)
        request_data = requestData.data.copy()
       
       
        company_instance = Company.objects.get(id=pk)
        for po_priority in request_data['po_priorities']:
            if po_priority['supplier']==None or  po_priority['supplier']=="":
                    request_data['po_priorities'] = []

        
        """************ data filtering for po_priorities*********************************"""
        po_priorities_update_data = list()
        po_priorities_create_data = list()
        unique = list()
        priority_unique=list()
        po_priorities_data =  request_data.pop('po_priorities')
        for po_priority_data in po_priorities_data:

            if "id" in  po_priority_data:
                unique.append(po_priority_data['supplier'])
                priority_unique.append(po_priority_data['priority'])
                po_priorities_update_data.append(po_priority_data)
              
            else: 
                po_priorities_create_data.append(po_priority_data)
        h1= unique
        len_supplier=len(h1)
        h2=list(set(unique))
        len_supplier_unique=len(h2)
        if len_supplier!=  len_supplier_unique:
            return Response("supplier and priority must be unique")

        m1=priority_unique
        len_priority=len(m1)
        m2=list(set(priority_unique))
        len_priority_unique=len(m2)
        if len_priority!= len_priority_unique:
            return Response("supplier and priority must be unique")
   
        
        for po_priority_update_data in po_priorities_update_data:
            po_priority_instance = PoPriority.objects.get(id=int(po_priority_update_data['id']))
            po_priority_update_serializer = PoPrioritySerializer(po_priority_instance, data=po_priority_update_data, partial=True, context={"request":request})
            if po_priority_update_serializer.is_valid():
                po_priority_update_serializer.save()
                
            else:
                return Response(po_priority_update_serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
        """*************************create po_priorities*********************************"""
        for po_priority_create_data in po_priorities_create_data:
            po_priority_create_data['company'] = company_instance.id
            po_priority_create_serializer = PoPrioritySerializer(data=po_priority_create_data,  context={"request":request})
           
            if po_priority_create_serializer.is_valid(raise_exception=True):
                po_priority_create_serializer.save()
                po_priority_instance = PoPriority.objects.get(id=int(po_priority_create_serializer.data['id']))
            else:
                return Response(po_priority_create_serializer.errors, status= status.HTTP_400_BAD_REQUEST)

        company_serializer = CompanySerializer(company_instance, data= request_data, partial=True, context={'request': request})
        if company_serializer.is_valid(raise_exception=True):
            
            company_serializer.save()
            return Response(company_serializer.data, status= status.HTTP_200_OK)
        else:
            return Response(company_serializer.errors, status= status.HTTP_400_BAD_REQUEST)
            

     

