
from unicodedata import name
from urllib import request
from rest_framework import status
from django.db import transaction
from rest_framework.generics import ListAPIView
# imported permissions
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
# third-party
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework import generics
from src.blood_test_order.models import BloodTestOrderMain
from src.blood_test.models import BloodTest
from src.user.models import User
from src.customer.models import Customer
from src.company.models import Company
from src.customer.serializers import RegisterCustomerSerializer
from src.item.models import Item, MedicineCategory,ProductCategory, SuperCategory
from rest_framework import  viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import FilterSet
import django_filters
from django_filters import DateFromToRangeFilter
from src.core_app.pagination import CustomPagination, CustomPaginationForBrand
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from src.customer_order.models import OrderMain
from src.customer_order.order_id_generator import  generate_customer_order_no
from src.blood_test_order.blood_test_order_id import generate_blood_test_order_no
# imported serializers
from src.user.views import FilterForUsers
from src.customer_order.serializers import SaveCustomerOrderSerializer
from src.blood_test_order.serializers import SaveBloodTestOrderSerializer
from .serializers import  PublicUserLoginSerializer, PublicUserLogoutSerializer, GetSuperCategorySerializer,\
                            PublicUserChangePasswordSerializer, GetMedicineItemSerializer, HomePageAppItemSerializer,\
                            GetMedicineCategorySerializer, GetProductCategorySerializer, PublicUserListSerializer,  \
                                GetBloodTestSerializer,  FeatureBrandItemSerializer, GetCompanyFeatureBrandSerializer,\
                                    ListCustomerSerializer, BetterDiscountItemSerializer, MostSaleItemSerializer

from .public_permissions import PublicUserChangePasswordPermissions, PublicUserViewPermissions,\
                  PublicUserRetrievePermission, AddToCartPermission
from simple_history.utils import update_change_reason
from src.customer.serializers import  UpdateCustomerSerializer,  RegisterPublicCustomerSerializer
from src.customer.customer_permissions import CustomerUpdatePermissions
from django.utils import timezone
from django.db.models import Sum, F
from src.sale.models import SaleDetail



class PublicUserRegisterView(viewsets.ModelViewSet):
    '''
    view for public customer user register
    '''
    permission_classes =  [AllowAny]
    queryset = Customer.objects.all()
    http_method_names = ['post']
    serializer_class =  RegisterPublicCustomerSerializer


    @transaction.atomic
    def create(self, request):
        # print(request.data['user']['user_name'], "this is request data")
       
        request.data['user']['first_name']= request.data['first_name']
        request.data['user']['last_name'] = request.data['last_name']
        request.data['user']['address'] = request.data['home_address']
         
        serializer = RegisterPublicCustomerSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def get_queryset(self):
    #     return User.objects.filter(user_type=2)

    # def post(self, request):
    #     user = request.data
    #     serializer = self.serializer_class(data=user, context={'request': request})
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     user_data = serializer.data
    #     return Response(user_data, status=status.HTTP_201_CREATED)



class PublicUserLoginView(APIView):
    
    permission_classes = [AllowAny]
    serializer_class = PublicUserLoginSerializer

    def get_queryset(self):
        return User.objects.all()

    def post(self, request):
        # print(request)
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):

            # saving user login information to log database
            # save_user_log(request, serializer.data['id'])
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PublicUserChangePasswordView(generics.UpdateAPIView):
    '''
    view for change password for public user
    '''
    permission_classes = [PublicUserChangePasswordPermissions]
    queryset = User.objects.filter(user_type=2)
    serializer_class = PublicUserChangePasswordSerializer


class PublicUserLogout(APIView):
    '''
    view for user logout
    '''
    permission_classes = [AllowAny]
    serializer_class =  PublicUserLogoutSerializer

    def get_queryset(self):
        return User.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"Logout successful"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PublicUserViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    read only viewset for user
    '''
    permission_classes = [PublicUserViewPermissions]
    queryset = User.objects.filter(user_type = 2)
    serializer_class = PublicUserListSerializer
    filter_class = FilterForUsers
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ["mobile_no", "user_name", 'email']
    ordering_fields = ['user_name',]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        user= self.request.user
        username = self.request.user.user_name
        return queryset if user.is_superuser else queryset.filter(user_name=username)


    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [PublicUserViewPermissions]
        elif self.action == 'retrieve':
            self.permission_classes = [PublicUserRetrievePermission]
        return super(self.__class__, self).get_permissions()


    
class FilterForPublicCustomerUpdate(django_filters.FilterSet):
    date = django_filters.DateFromToRangeFilter(field_name="created_date_ad")
    first_name = django_filters.CharFilter(field_name="first_name", lookup_expr='iexact')
   
    class Meta:
        model = Customer
        fields = ['id', 'user__user_name', 'user__email', 'phone_no','first_name','last_name']

class PublicUserCustomerUpdateView(viewsets.ModelViewSet):
    '''
    Model viewset for customer update
    '''
    permission_classes = [CustomerUpdatePermissions]
    queryset = Customer.objects.all()
    http_method_names = ['patch','get']
    serializer_class = UpdateCustomerSerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    filter_class =FilterForPublicCustomerUpdate
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ['phone_no','user__user_name']
    ordering_fields = [ 'first_name', ]

    def get_queryset(self):
        queryset = super().get_queryset()
        user= self.request.user
        # print(user, "this is user")
        return queryset if user.is_superuser else queryset.filter(user_id=user.id)
    
    def partial_update(self, request, pk , *args, **kwargs):
        '''
        Partial Update Method For Customer
        '''
        try:
            remarks = str(request.data['remarks']).strip()
            if len(remarks) <= 0:
                return Response({'remarks': 'Please give at least one word for remarks'},
                                status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'remarks': 'Please Provide remarks'}, status=status.HTTP_400_BAD_REQUEST)

     
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True, context={'request': request,
                                                                                                 'pk': instance.user.id}) 
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            '''
            for log history. Atleast one reason must be given if update is made
            '''
            update_change_reason(instance, remarks)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class FilterForGetSuperCategory(FilterSet):
    date = DateFromToRangeFilter(field_name="created_date_ad")
 
    class Meta:
        model = SuperCategory
        fields =  ['id','name']


class GetSuperCategoryViewset(viewsets.ModelViewSet):
        permission_classes = [AllowAny]  
        queryset = SuperCategory.objects.filter(active = True)
        serializer_class = GetSuperCategorySerializer
        http_method_names = ['get']
        filter_backends = (SearchFilter, DjangoFilterBackend)
        search_fields = ['name',]
        ordering_fields = ["name",]
        filter_class = FilterForGetSuperCategory
        pagination_class = CustomPagination


class FilterForAllItem(FilterSet):
    date = DateFromToRangeFilter(field_name="created_date_ad")
    brand_name = django_filters.CharFilter(lookup_expr='iexact')
    discount_rate = django_filters.RangeFilter(field_name="discount_rate")
    price = django_filters.RangeFilter(field_name="price")
    
    class Meta:
        model = Item
        fields =  ['id','product_category']


class CustomOrderingForAllItem(OrderingFilter):

    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)
       
        if ordering:
                for field in ordering:
                        if field=="price_high_to_low":
                                return queryset.order_by('-price')
                        elif field=="price_low_to_high":
                                return queryset.order_by('price')
                        elif field=="better_discount":
                                return queryset.order_by('-discount_rate')
        return queryset




class MedicineItemViewset(viewsets.ModelViewSet):
        permission_classes = [AllowAny]  
        queryset = Item.objects.filter(active = True,  product_category__is_medicine= True)
        serializer_class =  GetMedicineItemSerializer
        http_method_names = ['get']
        filter_backends = (SearchFilter, CustomOrderingForAllItem, DjangoFilterBackend)
        search_fields = ['brand_name','company__name']
        ordering_fields = ["price_high_to_low","price_low_to_high", 'better_discount']
        filter_class = FilterForAllItem
        pagination_class = CustomPagination



class FilterForHomePage(FilterSet):
    date = DateFromToRangeFilter(field_name="created_date_ad")
    brand_name = django_filters.CharFilter(lookup_expr='iexact')
    discount_rate = django_filters.RangeFilter(field_name="discount_rate")
    price = django_filters.RangeFilter(field_name="price")
    
    class Meta:
        model = Item
        fields =  ['id','product_category','company__name','company','product_category__super_category']

class FilterForGetCompany(FilterSet):
    date = DateFromToRangeFilter(field_name="created_date_ad")
    name = django_filters.CharFilter(lookup_expr='iexact')
   
    class Meta:
        model = Company
        fields =  ['id','name']


class SkincareCategoryItemViewset(viewsets.ReadOnlyModelViewSet):
        permission_classes = [AllowAny] #permission allowed to any
        serializer_class =  HomePageAppItemSerializer
        queryset = Item.objects.filter(company =  7, active = True ) | Item.objects.filter(company=323, active= True ) | Item.objects.filter(company=305, active= True ) | Item.objects.filter(company=166, active= True )
        http_method_names = ['get']
        filter_backends = (SearchFilter, CustomOrderingForAllItem, DjangoFilterBackend)
        search_fields = ['brand_name',"company__name"]
        ordering_fields = [ "price_high_to_low","price_low_to_high", 'better_discount']
        filter_class = FilterForHomePage
        pagination_class = CustomPagination


class BeautyCategoryItemViewset(viewsets.ReadOnlyModelViewSet):
        permission_classes = [AllowAny] #permission allowed to any
        serializer_class =  HomePageAppItemSerializer
        queryset = Item.objects.filter(company=	119, active= True ) | Item.objects.filter(company = 322, active= True) | Item.objects.filter(company = 328, active= True) | Item.objects.filter(company = 319, active= True) \
        | Item.objects.filter(company =  334 , active= True) | Item.objects.filter(company = 343, active= True) | Item.objects.filter(company = 42, active= True)

        filter_backends = (SearchFilter, CustomOrderingForAllItem, DjangoFilterBackend)
        search_fields = ['brand_name',"company__name"]
        ordering_fields = [ "price_high_to_low","price_low_to_high", 'better_discount']
        filter_class = FilterForHomePage
        pagination_class = CustomPagination


class HeathProductCategoryItemViewset(viewsets.ReadOnlyModelViewSet):
        permission_classes = [AllowAny] #permission allowed to any
        serializer_class =  HomePageAppItemSerializer
        queryset = Item.objects.filter(company=	135, active= True) | Item.objects.filter(company =263, active= True) | Item.objects.filter(company =92, active= True) 
        filter_backends = (SearchFilter, CustomOrderingForAllItem, DjangoFilterBackend)
        search_fields = ['brand_name',"company__name"]
        ordering_fields = [ "price_high_to_low","price_low_to_high", 'better_discount']
        filter_class = FilterForHomePage
        pagination_class = CustomPagination


class GetAllCategoryViewset(viewsets.ModelViewSet):
    permission_classes = [AllowAny]  
    queryset =  SuperCategory.objects.filter(active = True)
    serializer_class = GetSuperCategorySerializer
    http_method_names = ['get']

    def list(self, request, **kwargs):
        data = {} 
        medicine_categories = MedicineCategory.objects.filter(active=True) 
        medicine_categories_serializer = GetMedicineCategorySerializer(medicine_categories, many=True, context={"request": request})
        super_categories = SuperCategory.objects.filter(active= True)
        super_categories_serializer= GetSuperCategorySerializer(super_categories, many=True, context={"request": request})
        product_categories = ProductCategory.objects.filter(active= True)
        product_categories_serializer = GetProductCategorySerializer(product_categories, many=True, context={"request": request})
        data['medicine_categories'] = medicine_categories_serializer.data
        data['super_categories'] = super_categories_serializer.data
        data['product_categories'] = product_categories_serializer.data
        return Response(data, status=status.HTTP_200_OK)


class FilterForBloodTestItem(FilterSet):
    date = DateFromToRangeFilter(field_name="created_date_ad")
 
    class Meta:
        model = BloodTest
        fields =  ['id','name', "department","specimen"]    

class BloodTestItemViewset(viewsets.ReadOnlyModelViewSet):
        permission_classes = [AllowAny] #permission allowed to any
        serializer_class =  GetBloodTestSerializer
        queryset = BloodTest.objects.filter(active=True)
        http_method_names = ['get']
        filter_backends = (SearchFilter, CustomOrderingForAllItem, DjangoFilterBackend)
        search_fields = ['name',"specimen","department"]
        ordering_fields = [ "id","price"]
        filter_class = FilterForBloodTestItem
        pagination_class = CustomPagination


class BrandWiseItemViewset(viewsets.ReadOnlyModelViewSet):
        permission_classes = [AllowAny]
        serializer_class = FeatureBrandItemSerializer
        queryset = Item.objects.filter(company__feature_brand = True, active= True)
        http_method_names = ['get']
        filter_backends = (SearchFilter, CustomOrderingForAllItem, DjangoFilterBackend)
        search_fields = ['brand_name',"company__name"]
        ordering_fields = [ "price_high_to_low","price_low_to_high", 'better_discount']
        filter_class = FilterForHomePage
        pagination_class = CustomPagination



class BrandListViewset(viewsets.ReadOnlyModelViewSet):
        permission_classes = [AllowAny]
        serializer_class = GetCompanyFeatureBrandSerializer
        queryset = Company.objects.filter(feature_brand = True)
        http_method_names = ['get']
        filter_backends = (SearchFilter, CustomOrderingForAllItem, DjangoFilterBackend)
        search_fields = ['id','name']
        ordering_fields = [ "id"]
        filter_class = FilterForGetCompany
        pagination_class = CustomPaginationForBrand


# @csrf_exempt
# def add_to_cart_list(request):
       
#     if request.method == 'POST':
#         data = JSONParser().parse(request)
#         if data["is_medicine_order"]==True:
#             serializer = SaveCustomerOrderSerializer(data=data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return JsonResponse(serializer.data, status=201)
#             return JsonResponse(serializer.errors, status=400)

#         elif data["is_blood_test_order"]==True:
#             serializer = SaveBloodTestOrderSerializer(data=data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return JsonResponse(serializer.data, status=201)
#             return JsonResponse(serializer.errors, status=400)


class AddToCartListView(viewsets.ModelViewSet):
    permission_classes = [AddToCartPermission]
    http_method_names = ['post',]
    serializer_class = SaveCustomerOrderSerializer
    queryset = OrderMain.objects.all()


    @transaction.atomic
    def create(self, request, *args, **kwargs):
        
        if request.data['is_customer_order']==True and request.data['is_blood_test_order']==True:
    
            try:
                customer_order_main = request.data.pop('customer_order_main')
            except KeyError:
                return Response('Provide customer order data in customer_order_main key',
                                status=status.HTTP_400_BAD_REQUEST)

            try:
                blood_test_order = request.data.pop('blood_test_order')
            except KeyError:
                return Response('Provide blood test data in blood_test_order key',
                                status=status.HTTP_400_BAD_REQUEST)

        
            alt_phone_no= customer_order_main['alt_phone_no']
            customer_data = Customer.objects.get(id = customer_order_main['customer']) 
            customer_data.alt_phone_no =  alt_phone_no
            customer_data.save()

            customer_order_main['order_no'] =  generate_customer_order_no()
            blood_test_order['blood_test_order_no'] = generate_blood_test_order_no()

           
            if  blood_test_order['blood_test']== []:
                blood_test_order['is_blood_test']=False
            else:
                    blood_test_order['is_blood_test']= True

            if  blood_test_order['test_package']== []:
                    blood_test_order['is_test_package']=False
            else:
                    blood_test_order['is_test_package']=True
           
            co_order_serializer = SaveCustomerOrderSerializer(data= customer_order_main, context={'request': request})
            blood_order_serializer = SaveBloodTestOrderSerializer(data= blood_test_order, context={'request': request})
            if co_order_serializer.is_valid(raise_exception=True):
                    co_order_serializer.save()
                
                    if blood_order_serializer.is_valid(raise_exception=True):
                            blood_order_serializer.save()
                            return Response(co_order_serializer.data, status=201)

                    else:
                        return Response(blood_order_serializer.errors, status=400)

            else:
                return Response(co_order_serializer.errors, status=400)

        if request.data['is_customer_order']==True and request.data['is_blood_test_order']==False:
            
            try:
                customer_order_main = request.data.pop('customer_order_main')
            except KeyError:
                return Response('Provide customer order data  in customer_order_main key',
                                status=status.HTTP_400_BAD_REQUEST)

            alt_phone_no= customer_order_main['alt_phone_no']
            customer_data = Customer.objects.get(id = customer_order_main['customer']) 
            customer_data.alt_phone_no =  alt_phone_no
            customer_data.save()

            customer_order_main['order_no'] =  generate_customer_order_no()
            co_order_serializer = SaveCustomerOrderSerializer(data= customer_order_main, context={'request': request})

            if co_order_serializer.is_valid(raise_exception=True):
                    co_order_serializer.save()
                    return Response(co_order_serializer.data, status=201)
            else:
                return Response(co_order_serializer.errors, status=400)


        if request.data['is_blood_test_order']==True and request.data['is_customer_order']==False:
            try:
                blood_test_order = request.data.pop('blood_test_order')
            except KeyError:
                return Response('Provide blood test data in blood_test_order key',
                                status=status.HTTP_400_BAD_REQUEST)

            try:
                customer_order_main = request.data.pop('customer_order_main')
            except KeyError:
                return Response('Provide customer order data in customer_order_main key',
                                status=status.HTTP_400_BAD_REQUEST)

            blood_test_order['blood_test_order_no'] = generate_blood_test_order_no()
            if  blood_test_order['blood_test']== []:
                blood_test_order['is_blood_test']=False
            else:
                    blood_test_order['is_blood_test']= True

            if  blood_test_order['test_package']== []:
                    blood_test_order['is_test_package']=False
            else:
                    blood_test_order['is_test_package']=True


            alt_phone_no=  customer_order_main['alt_phone_no']
            customer_data = Customer.objects.get(id = blood_test_order['customer']) 
            customer_data.alt_phone_no =  alt_phone_no
            customer_data.save()

            blood_order_serializer = SaveBloodTestOrderSerializer(data= blood_test_order, context={'request': request})
            if blood_order_serializer.is_valid(raise_exception=True):
                            blood_order_serializer.save()
                            return Response(blood_order_serializer.data, status=201)

            else:
                return Response(blood_order_serializer.errors, status=400)
          


class ListPublicUserViewSet(viewsets.ReadOnlyModelViewSet):
  
    permission_classes = [PublicUserViewPermissions]
    queryset = Customer.objects.all()
    serializer_class = ListCustomerSerializer
    # filter_class = FilterForUsers
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ["id",]
    # ordering_fields = ['user_name',]
    # pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        user= self.request.user
        user_id = self.request.user.id
        return  queryset.filter(user=user_id)
        # return queryset if user.is_superuser else queryset.filter(user=user_id)       




class SpecialOfferItemViewset(viewsets.ModelViewSet):
        permission_classes = [AllowAny]  
        queryset = Item.objects.filter(discount_rate__gte=10.00)
        serializer_class =   BetterDiscountItemSerializer
        http_method_names = ['get']
        filter_backends = (SearchFilter, CustomOrderingForAllItem, DjangoFilterBackend)
        search_fields = ['brand_name','company__name']
        ordering_fields = ["price_high_to_low","price_low_to_high", 'better_discount']
        filter_class = FilterForAllItem
        pagination_class = CustomPagination



class FilterForTopSaleItem(FilterSet):
    date = DateFromToRangeFilter(field_name="created_date_ad")
  
    class Meta:
        model = SaleDetail
        fields =  ['item__id','item__brand_name','item__company__name']



class  MostSaleItemViewSet(viewsets.ModelViewSet):
        permission_classes = [AllowAny]  
        serializer_class =   MostSaleItemSerializer
        queryset= SaleDetail.objects.all()
        http_method_names = ['get']
        filter_backends = (SearchFilter,OrderingFilter, DjangoFilterBackend)
        search_fields = ['item__brand_name','item__company__name']
        ordering_fields = ['qty']
        filter_class = FilterForTopSaleItem
        pagination_class = CustomPagination
        

        # def get_queryset(self):
        #     return  SaleDetail.objects.filter(created_date_ad__month=timezone.now().month, sale_main__sale_type=1).distinct('item')

        def list(self, request):
            queryset = SaleDetail.objects.filter(created_date_ad__year=timezone.now().year, sale_main__sale_type=1).distinct('item')
            serializer = MostSaleItemSerializer(queryset, many=True)
            serializer_data = sorted(
                serializer.data, key=lambda k: k['total_sale_qty'], reverse=True)
            return Response(serializer_data)


        




      

