'''
model viewset class for item app
'''
# Django-Rest_framework

from rest_framework.response import Response
from rest_framework import viewsets, status
from django_filters.rest_framework import DjangoFilterBackend, DateFromToRangeFilter
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import FilterSet
import django_filters
from rest_framework.response import Response
from drf_nested_forms.utils import NestedForm

# imported serializers
from .serializers import GetItemUnitSerializer, GetMedicineCategorySerializer, GetProductSerializer, GetSuperCategorySerializer, UnitSerializer,  GenericNameSerializer, ItemSerializer

from .serializers import StrengthSerializer, GetCompanySerializer, GetSupplierSerializer, GetMedicineFormSerializer,ItemUnitSerializer,  DeletePoPrioritySerializer,\
    SuperCategorySerializer, ProductCategorySerializer, MedicineCategorySerializer, MedicineFormSerializer, PoPrioritySerializer, GenericStrengthSerializer, GenericStrengthMapSerializer,\
        GetItemSerializer
# imported models
from .models import MedicineForm, Strength, Unit,  GenericName, Item, GenericStrength,\
    SuperCategory, ProductCategory, MedicineCategory, PoPriority, ItemUnit
from .item_permissions import UnitPermission, GenericNamePermission, ItemPermission
from .item_permissions import  MedicineCategoryPermission, ProductCategoryPermission, GenericStrengthPermission, \
SuperCategoryPermission, MedicineFormPermission, PoPriorityPermission, StrengthPermission, ItemUnitPermission
from src.company.models import Company
from src.supplier.models import Supplier
from django.db import transaction
from django.db.models import Prefetch
# for log
from simple_history.utils import update_change_reason
from rest_framework.decorators import action
from drf_nested_forms.utils import NestedForm
from src.core_app.pagination import CustomPagination



class GetItemDataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Item.objects.filter(active= True).order_by('id')
    serializer_class = GetItemSerializer
    pagination_class = CustomPagination
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ['brand_name', 'ws_unit']
    

# class FilterForGetItemBilling(FilterSet):
    
   
#     date = DateFromToRangeFilter(field_name="created_date_ad")
   
#     class Meta:
#         model = Unit
#         fields = ['name','active', 'short_form']


class FilterForUnit(FilterSet):
    '''
    custom filter for unit
    '''
   
    date = DateFromToRangeFilter(field_name="created_date_ad")
    name = django_filters.CharFilter(lookup_expr='iexact')
    short_form = django_filters.CharFilter(lookup_expr='iexact')
    class Meta:
        model = Unit
        fields = ['name','active', 'short_form']

class UnitViewSet(viewsets.ModelViewSet):
    '''
    model viewset for unit
    '''
    permission_classes = [UnitPermission]
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    filter_class = FilterForUnit
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ['name', 'short_form']
    ordering_fields = ['id', 'name', 'short_form']
    http_method_names = ['get', 'head', 'post', 'patch']



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
            '''
            for log history. Atleast one reason must be given if update is made
            '''
            update_change_reason(instance, remarks)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FilterForItemUnit(FilterSet):
    '''
    custom filter for unit
    '''
    date = DateFromToRangeFilter(field_name="created_date_ad")
    name = django_filters.CharFilter(lookup_expr='iexact')
    short_form = django_filters.CharFilter(lookup_expr='iexact')
    class Meta:
        model = ItemUnit
        fields = ['name','active', 'short_form']

class ItemUnitViewSet(viewsets.ModelViewSet):
    '''
    model viewset for unit
    '''
    permission_classes = [ItemUnitPermission]
    queryset = ItemUnit.objects.all()
    serializer_class = ItemUnitSerializer
    filter_class = FilterForItemUnit
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ['name', 'short_form']
    ordering_fields = ['id', 'name', 'short_form']
    http_method_names = ['get', 'head', 'post', 'patch','delete']


    
    def destroy(self, request, *args, **kwargs):
        
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

       
    

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
            '''
            for log history. Atleast one reason must be given if update is made
            '''
            update_change_reason(instance, remarks)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FilterForGenericName(FilterSet):
    '''
    custom filter for generic name
    '''
    date = DateFromToRangeFilter(field_name="created_date_ad")
    name = django_filters.CharFilter(lookup_expr='iexact')
    class Meta:
        model = GenericName
        fields = ['name','active']

class GenericNameViewSet(viewsets.ModelViewSet):
    '''
    model viewset for generic name
    '''
    # parser_classes = (JSONParser, NestedMultiPartParser, )
    permission_classes = [GenericNamePermission]
    queryset = GenericName.objects.filter(archived = False)
    serializer_class = GenericNameSerializer
    filter_class = FilterForGenericName
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ['name',]
    ordering_fields = ['id', 'name']
    http_method_names = ['get', 'head', 'post', 'patch']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(generic_strength__archived=False).prefetch_related(
                Prefetch(
                    "generic_strength",
                    queryset=GenericStrength.objects.filter(archived=False),
                ),
            ).distinct()
        return queryset

   
    @transaction.atomic
    def partial_update(self, request, pk, *args, **kwargs):
        
        generic_name_instance = GenericName.objects.get(id=pk)
        
        try:
            remarks = str(request.data['remarks']).strip()
            if len(remarks) <= 0:
                return Response({'remarks': 'Please give at least one word for remarks'},
                                status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'remarks': 'Please Provide remarks'}, status=status.HTTP_400_BAD_REQUEST)

        generic_strength_update_data = list()
        generic_strength_create_data = list()
        generic_strength_data =  request.data.pop('generic_strength')
        for generic_data in  generic_strength_data:
            if "id" in  generic_data:
                  generic_strength_update_data.append(generic_data)
            else: 
                  generic_strength_create_data.append(generic_data)

        strength_ids=[]
        for  generic in generic_strength_update_data:
            strength_ids.append(generic['id'])

        generic_strength_data= GenericStrength.objects.filter(generic_name=generic_name_instance.id).exclude(id__in= strength_ids)

        for strength_data in generic_strength_data:
            strength_data.archived = True
            strength_data.save()
            
        for generic_update_data in  generic_strength_update_data:
            # if generic_update_data==[] or None:
            #       return Response([], status= status.HTTP_200_OK)

            generic_strength_instance = GenericStrength.objects.get(id=int(generic_update_data['id']))
         
            generic_update_serializer = GenericStrengthMapSerializer(generic_strength_instance, data=generic_update_data, partial=True, context={"request":request})
            if  generic_update_serializer.is_valid():
                generic_update_serializer.save()
                
            else:
                return Response(generic_update_serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
        for  generic_create_data in generic_strength_create_data:
            generic_create_data['generic_name'] = generic_name_instance.id
            generic_create_serializer = GenericStrengthSerializer(data=generic_create_data,  context={"request":request})
           
            if generic_create_serializer.is_valid(raise_exception=True):
                generic_create_serializer.save()
                generic_strength_instance = GenericStrength.objects.get(id=int(generic_create_serializer.data['id']))
            else:
                return Response(generic_create_serializer.errors, status= status.HTTP_400_BAD_REQUEST)

        generic_name_serializer = GenericNameSerializer(generic_name_instance, data= request.data, partial=True)

        if  generic_name_serializer.is_valid(raise_exception=True):
            generic_name_serializer.save()  
            queryset = GenericName.objects.filter(generic_strength__archived=False).prefetch_related(
                    Prefetch(
                        "generic_strength",
                        queryset=GenericStrength.objects.filter(archived=False),
                        ),).distinct().get(id =generic_name_instance.id)
         
            generic_name_serializer = GenericNameSerializer(queryset)
            return Response(generic_name_serializer.data, status= status.HTTP_200_OK)
        else:
            return Response(generic_name_serializer.errors, status= status.HTTP_400_BAD_REQUEST)    
  
   
class FilterForItem(FilterSet):
    '''
    custom filter for item
    '''
    date = DateFromToRangeFilter(field_name="created_date_ad")
    brandName = django_filters.CharFilter(lookup_expr='iexact', field_name="brand_name") 
    class Meta:
        model = Item
        fields = ['company','item_unit']
                  

class ItemViewSet(viewsets.ModelViewSet):
    '''
    model viewset for item
    '''
    '''
    custom permission for item
    '''
    permission_classes = [ItemPermission]
    queryset = Item.objects.filter(archived = False).select_related('item_unit','medicine_form','company')
    serializer_class = ItemSerializer
    filter_class = FilterForItem
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ['brand_name','company__name']
    ordering_fields = ['id', 'brand_name']
    http_method_names = ['get','head' ,'post','patch']
   

    @action(url_path="get-data", detail=False)
    def get_data(self, request):  
        data = {} 
        suppliers = Supplier.objects.filter(active=True)
        suppliers_serializer = GetSupplierSerializer(suppliers, many=True)
        company = Company.objects.filter(active=True).order_by('name')
        company_serializer = GetCompanySerializer(company, many=True)
        medicine_form = MedicineForm.objects.filter(active=True).order_by('name')
        medicine_form_serializer = GetMedicineFormSerializer(medicine_form, many=True)
        data['medicine_form'] = medicine_form_serializer.data
        data['company '] = company_serializer.data
        data['suppliers'] = suppliers_serializer.data
        return Response(data, status=status.HTTP_200_OK)


    
    @action(url_path="get-primary-form-data", detail=False)
    def get_primary_form_data(self, request):  
        data = {} 
        companies = Company.objects.filter(active=True).order_by('name')
        company_serializer = GetCompanySerializer(companies, many=True)
        item_units = ItemUnit.objects.filter(active=True)
        item_unit_serializer = GetItemUnitSerializer(item_units, many=True)
        super_categories = SuperCategory.objects.filter(active=True)
        super_category_serializer = GetSuperCategorySerializer(super_categories, many=True)
        medicine_categories = MedicineCategory.objects.filter(active=True)
        medicine_category_serializer = GetMedicineCategorySerializer( medicine_categories, many=True)
        product_categories = ProductCategory.objects.filter(active=True)
        product_category_serializer = GetProductSerializer(product_categories, many=True)
       

        data['companies'] = company_serializer.data
        data['item_units'] =  item_unit_serializer.data
        data['super_categories'] =   super_category_serializer.data
        data['medicine_categories'] = medicine_category_serializer.data
        data['product_categories'] = product_category_serializer.data
        return Response(data, status=status.HTTP_200_OK)


    
    @action(url_path="get-secondary-form-data", detail=False)
    def get_secondary_form_data(self, request):  
        data = {} 
        generic_name_strengths = GenericStrength.objects.all()
        generic_strengths_serializer = GenericStrengthSerializer(generic_name_strengths, many=True)
        medicine_forms = MedicineForm.objects.filter(active=True)
        medicine_form_serializer = GetMedicineFormSerializer(medicine_forms, many=True)
        data['medicine_forms'] = medicine_form_serializer.data
        data['generic_name_strengths'] =  generic_strengths_serializer.data
        return Response(data, status=status.HTTP_200_OK)
   

    def create(self, request, *args, **kwargs): 
        '''
        create method for item
        '''
        requestData = NestedForm(request.data)
        if requestData.is_nested(raise_exception=False):
            data = requestData.data
        else:
            data = request.data.dict()
        if data['product_category']!="":
            try:
                product_category_id_list = data['product_category']   
                product_categories = ProductCategory.objects.filter(id__in = product_category_id_list) 

            except KeyError:
                return Response({'key_error': 'please provide list of product categories id list'},
                                status=status.HTTP_400_BAD_REQUEST)
            is_medicine = False
            for product_category in product_categories:
                    # print(product_category.is_medicine) 
                    if product_category.is_medicine is True:
                        is_medicine = True
                        if data['medicine_form']==None or data['generic_name']==None or data['medicine_form']=='' or data['generic_name']=='':         
                                return Response({'key_error':'please provide generic name and medicine form Keys'},
                                status=status.HTTP_400_BAD_REQUEST)

                        if "medicine_form" not in data or "generic_name" not in data:
                            return Response({'key_error': 'please provide generic name and medicine form Keys with value'},
                                status=status.HTTP_400_BAD_REQUEST)
            # data = requestData.data.copy()
            if not is_medicine:
                    if data['medicine_form'] != "" or data['generic_name'] != "":
                            return Response({'key_error': 'please provide generic name and medicine form as blank'},
                                status=status.HTTP_400_BAD_REQUEST)
                    else:
                        data['generic_name'] = []
        else:
            data['product_category'] = []
            data['generic_name'] = []
        
        serializer = ItemSerializer(data=data, context={'request': request})
        if serializer.is_valid(raise_exception=True): 
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 

    def partial_update(self, request, *args, **kwargs):

        requestData = NestedForm(request.data)
        if requestData.is_nested(raise_exception=False):
            data = requestData.data
        else:
            data = request.data.dict()
            # print(data)
        try:
            remarks = str(request.data['remarks']).strip()
            if len(remarks) <= 0:
                return Response({'remarks': 'Please give at least one word for remarks'},
                                status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'remarks': 'Please Provide remarks'}, status=status.HTTP_400_BAD_REQUEST)
        # if "image" not in data:
        #     data['image']=""
        if data['product_category']!="":
            try:
                product_category_id_list = data['product_category']   
                product_categories = ProductCategory.objects.filter(id__in = product_category_id_list) 

            except KeyError:
                return Response({'key_error': 'please provide list of product categories id list'},
                                status=status.HTTP_400_BAD_REQUEST)
            is_medicine = False
            for product_category in product_categories:
                    # print(product_category.is_medicine) 
                    if product_category.is_medicine is True:
                        is_medicine = True
                        if data['medicine_form']==None or data['generic_name']==None or data['medicine_form']=='' or data['generic_name']=='':         
                                return Response({'key_error':'please provide generic name and medicine form Keys'},
                                status=status.HTTP_400_BAD_REQUEST)

                        if "medicine_form" not in data or "generic_name" not in data:
                            return Response({'key_error': 'please provide generic name and medicine form Keys with value'},
                                status=status.HTTP_400_BAD_REQUEST)
            # data = requestData.data.copy()
            if not is_medicine:
                    if data['medicine_form'] != "" or data['generic_name'] != "":
                            return Response({'key_error': 'please provide generic name and medicine form as blank'},
                                status=status.HTTP_400_BAD_REQUEST)
                    else:
                        data['generic_name'] = []
        else:
            data['product_category'] = []
            data['generic_name'] = []
       
        
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=data, partial=True, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            '''
            for log history. Atleast one reason must be given if update is made
            '''
            update_change_reason(instance, remarks)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    


class FilterForSuperCategory(FilterSet):
    '''
    custom filter for super category
    '''
    date = DateFromToRangeFilter(field_name="created_date_ad")
    name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = SuperCategory
        fields = ['name',]

class SuperCategoryViewSet(viewsets.ModelViewSet):
    '''
    model viewset for supercategory
    '''
    permission_classes = [SuperCategoryPermission]
    queryset = SuperCategory.objects.filter(archived = False)
    serializer_class = SuperCategorySerializer
    filter_class = FilterForSuperCategory
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ['name', ]
    ordering_fields = ['id', 'name']
    http_method_names = ['get', 'head', 'post', 'patch']



    def partial_update(self, request, *args, **kwargs):
        '''
        Partial update method for Super Category
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



class FilterForProductCategory(FilterSet):
    '''
    custom filter for product category
    '''
    date = DateFromToRangeFilter(field_name="created_date_ad")
    name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = ProductCategory
        fields = ['name',]


class ProductCategoryViewSet(viewsets.ModelViewSet):
    '''
    model viewset for product category
    '''
    permission_classes = [ProductCategoryPermission]
    queryset = ProductCategory.objects.filter(archived = False)
    serializer_class = ProductCategorySerializer
    filter_class = FilterForProductCategory
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ['name', ]
    ordering_fields = ['id', 'name']
    http_method_names = ['get', 'head', 'post', 'patch']


       
    def partial_update(self, request, *args, **kwargs):
        '''
        Partial update method of product category
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


class FilterForMedicineCategory(FilterSet):
    '''
    custom filter for medicine category
    '''
    date = DateFromToRangeFilter(field_name="created_date_ad")
    name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = MedicineCategory
        fields = ['name',]

class MedicineCategoryViewSet(viewsets.ModelViewSet):
    '''
    model viewset for medicine category
    '''
    permission_classes = [MedicineCategoryPermission]
    queryset = MedicineCategory.objects.filter(archived = False)
    serializer_class = MedicineCategorySerializer
    filter_class = FilterForMedicineCategory
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ['name', ]
    ordering_fields = ['id', 'name']
    http_method_names = ['get', 'head', 'post', 'patch']



    def partial_update(self, request, *args, **kwargs):
        '''
        Partial update method for Medicine Category
        '''
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
            '''
            for log history. Atleast one reason must be given if update is made
            '''
            update_change_reason(instance, remarks)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class FilterForMedicineForm(FilterSet):
    '''
    custom filter for medicine form
    '''
    date = DateFromToRangeFilter(field_name="created_date_ad")
    name = django_filters.CharFilter(lookup_expr='iexact')
    
    class Meta:
        model = MedicineForm
        fields = ['id', 'name', 'active']
  
class MedicineFormViewSet(viewsets.ModelViewSet):
    '''
    model viewset for medicine form
    '''
    permission_classes = [MedicineFormPermission]
    queryset = MedicineForm.objects.filter(archived = False)
    serializer_class = MedicineFormSerializer
    filter_class = FilterForMedicineForm
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ['name', ]
    ordering_fields = ['id', 'name']
    http_method_names = ['get', 'head', 'post', 'patch']


    def partial_update(self, request, *args, **kwargs):
        ''''
        Partial Update method for Medicine Form
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


class FilterForPoPriority(FilterSet):
    '''
    custom filter for medicine form
    '''
    date = DateFromToRangeFilter(field_name="created_date_ad")
    
    class Meta:
        model = PoPriority
        fields = ['id', 'supplier__name','company__name', 'priority','active']
  

class PoPriorityViewSet(viewsets.ModelViewSet):
    '''
    model viewset for po priority
    '''
    permission_classes = [PoPriorityPermission]
    queryset = PoPriority.objects.filter(archived = False)
    serializer_class = PoPrioritySerializer
    filter_class = FilterForPoPriority
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ['id', 'priority','supplier','item']
    ordering_fields = ['id', 'priority']
    http_method_names = ['get','head', 'delete']


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.archived=True
        serializer =  DeletePoPrioritySerializer(instance, data=request.data,  partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Deleted Po Priority Successfully')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class FilterForStrength(FilterSet):
    '''
    custom filter for strength
    '''
    date = DateFromToRangeFilter(field_name="created_date_ad")
    strength= django_filters.CharFilter(lookup_expr='iexact')
    
    class Meta:
        model = Strength
        fields = ['id', 'strength','unit']
        
class StrengthViewSet(viewsets.ModelViewSet):
    '''
    model viewset for strength
    '''
    permission_classes = [StrengthPermission]
    queryset = Strength.objects.filter(archived = False)
    serializer_class = StrengthSerializer
    filter_class = FilterForStrength
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ['strength', 'unit__name']
    ordering_fields = ['id', 'strength']
    http_method_names = ['get','head','post','patch']


    
    def partial_update(self, request, *args, **kwargs):
        '''
        Partial Update Method For Strength
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



class FilterForGenericStrength(FilterSet):
    '''
    custom filter for medicine form
    '''
    date = DateFromToRangeFilter(field_name="created_date_ad")
    
    class Meta:
        model = GenericStrength
        fields = ['id', ]

class GenericStrengthViewSet(viewsets.ModelViewSet):
    
    permission_classes = [GenericStrengthPermission]
    queryset = GenericStrength.objects.filter(archived= False)
    serializer_class = GenericStrengthSerializer
    filter_class = FilterForGenericStrength
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ['id', ]
    ordering_fields = ['id', ]
    http_method_names = ['get','head','post','patch']


    def partial_update(self, request, *args, **kwargs):
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
            # update_change_reason(instance, remarks)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    