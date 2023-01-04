# third-party
from rest_framework import viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
# imported serializers
from .serializers import SupplierSerializer, SupplierContactSerializer
import django_filters
from django.db import transaction

# imported models
from .models import Supplier, SupplierContact
from .supplier_permissions import SupplierPermission, SupplierContactPermission

# for log
from simple_history.utils import update_change_reason

# filter
class FilterForSupplier(django_filters.FilterSet):
    date = django_filters.DateFromToRangeFilter(field_name="created_date_ad")
    name = django_filters.CharFilter(lookup_expr='iexact')
    address = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Supplier
        fields = ['phone_no', 'name', 'active', 'pan_vat_no']

# viewset for supplier
class SupplierViewSet(viewsets.ModelViewSet):
    '''
    viewset for supplier
    '''
    permission_classes = [SupplierPermission]
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filter_class = FilterForSupplier
    search_fields = ['name', 'address', 'pan_vat_no']
    ordering_fields = ['id', 'name']
    http_method_names = ['get', 'head', 'post', 'patch']


    def create(self, request):
        '''
        this method will create supplier
        '''
        map_location = request.data['map_location']
        
        try:
            if request.data['map_location']!="" or not None:
                # print('hello this is')
                longitude = map_location.split(",")[0]
                latitude = map_location.split(",")[1]
                request.data['longitude'] = longitude
                request.data['latitude'] = latitude

        except: 
            request.data['longitude'] = ""
            request.data['latitude'] = ""

        
        serializer = SupplierSerializer(data=request.data,  context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       

    @transaction.atomic
    def partial_update(self, request, pk, *args, **kwargs):
        '''
        this method will update customer
        '''
        supplier_instance = Supplier.objects.get(id=pk)
        map_location = request.data['map_location']
        try:
            if request.data['map_location']!="" or not None:
                # print('hello this is')
                longitude = map_location.split(",")[0]
                latitude = map_location.split(",")[1]
                request.data['longitude'] = longitude
                request.data['latitude'] = latitude

        except: 
            request.data['longitude'] = ""
            request.data['latitude'] = ""

        try:
            remarks = str(request.data['remarks']).strip()
            if len(remarks) <= 0:
                return Response({'remarks': 'Please give at least one word for remarks'},
                                status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'remarks': 'Please Provide remarks'}, status=status.HTTP_400_BAD_REQUEST)


        """************ data filtering for supplier contacts*********************************"""
        supplier_contacts_update_data = list()
        supplier_contacts_create_data = list()
        supplier_contacts_data =  request.data.pop('supplier_contacts')
        for supplier_contact_data in supplier_contacts_data:

            if "id" in   supplier_contact_data:
                supplier_contacts_update_data.append(supplier_contact_data)
            else: 
                 supplier_contacts_create_data.append(supplier_contact_data)

        """******************************update  supplier contacts*********************************"""
        for supplier_contact_update_data in  supplier_contacts_update_data:
            supplier_contact_instance = SupplierContact.objects.get(id=int(supplier_contact_update_data['id']))
            supplier_contact_update_serializer = SupplierContactSerializer(supplier_contact_instance, data=supplier_contact_update_data, partial=True, context={"request":request})
            if  supplier_contact_update_serializer.is_valid():
                supplier_contact_update_serializer.save()
                
            else:
                return Response(supplier_contact_update_serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
        """******************************create supplier contacts*********************************"""
        for  supplier_contact_create_data in supplier_contacts_create_data:
            supplier_contact_create_data['supplier'] = supplier_instance.id
            supplier_contact_create_serializer = SupplierContactSerializer(data=supplier_contact_create_data,  context={"request":request})
           
            if supplier_contact_create_serializer.is_valid(raise_exception=True):
                supplier_contact_create_serializer.save()
                supplier_contact_instance = SupplierContact.objects.get(id=int(supplier_contact_create_serializer.data['id']))
            else:
                return Response(supplier_contact_create_serializer.errors, status= status.HTTP_400_BAD_REQUEST)

        supplier_serializer = SupplierSerializer(supplier_instance, data= request.data, partial=True)
        if supplier_serializer.is_valid(raise_exception=True):
            
            supplier_serializer.save()
            return Response(supplier_serializer.data, status= status.HTTP_200_OK)
        else:
            return Response(supplier_serializer.errors, status= status.HTTP_400_BAD_REQUEST)    



class FilterForSupplierContact(django_filters.FilterSet):
    '''
    custom filter class for supplier contact
    '''
    date = django_filters.DateFromToRangeFilter(field_name="created_date_ad")
    class Meta:
        model = SupplierContact
        fields = ['supplier', 'contact_person', 'active']


class SupplierContactViewSet(viewsets.ModelViewSet):
    '''
    viewset for supplier contact
    '''
    permission_classes = [SupplierContactPermission]
    queryset = SupplierContact.objects.all()
    serializer_class = SupplierContactSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filter_class = FilterForSupplierContact
    search_fields = ['supplier', 'contact_person']
    ordering_fields = ['id', 'contact_person']
    http_method_names = ['get', 'head', 'post', 'patch']


    def partial_update(self, request, *args, **kwargs):
        '''
        partial update method for supplier contact
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
