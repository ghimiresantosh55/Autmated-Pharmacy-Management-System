from pickle import TRUE
from django.shortcuts import render
from rest_framework import viewsets
from django.db import transaction
from rest_framework import status
# filter
from django_filters.rest_framework import DjangoFilterBackend,  DateFromToRangeFilter
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from src.blood_test.models import BloodTest, TestPackage
from .serializers import SaveBloodTestOrderSerializer,  DeleteBloodTestOrderSerializer,  QuickUpdateBloodTestOrderSerializer
from src.blood_test_order.models import BloodTestOrderMain
from django_filters import rest_framework as filters
from .blood_test_order_id import generate_blood_test_order_no
from .blood_test_order_permissions import  SaveBloodTestOrderPermission , QuickUpdateBloodTestOrderOrderPermission
from rest_framework import generics
from simple_history.utils import update_change_reason
from rest_framework.decorators import action

class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass

class RangeFilterForBloodTestOrderMain(filters.FilterSet):
    date = DateFromToRangeFilter(field_name="created_date_ad")
    delivery_status_in = NumberInFilter(field_name='delivery_status', lookup_expr='in')
  
    
    class Meta:
        model = BloodTestOrderMain
        fields = ['customer__first_name','customer__last_name', 'customer__phone_no', 'delivery_person', 'delivery_status_in','blood_test_order_no','amount_status', 'order_location']


class SaveBloodTestOrderMainViewSet(viewsets.ModelViewSet):
    permission_classes = [SaveBloodTestOrderPermission]   
    queryset = BloodTestOrderMain.objects.filter(archived=False).select_related("delivery_person","customer")
    serializer_class =  SaveBloodTestOrderSerializer
    filter_class = RangeFilterForBloodTestOrderMain
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['id',]
    search_fields = ['customer__first_name','customer__last_name','customer__phone_no','blood_test_order_no','amount_status','order_location']
    http_method_names = ['get', 'post', 'patch']

    @transaction.atomic
    def create(self, request, *args, **kwargs): 
        blood_test_price_list= []
        test_package_price_list =[]
        blood_tests=request.data['blood_test']
        test_packages= request.data['test_package']
        for blood_test in blood_tests:
            blood_test_obj= BloodTest.objects.filter(id=blood_test)
            for test_obj in  blood_test_obj:
                prices= test_obj.price
                blood_test_price_list.append(prices)

            sub_total_test = sum(blood_test_price_list)
            # print(sub_total_test, " this is sub total")
                   
        for test_package in test_packages:
            test_pack_obj= TestPackage.objects.filter(id = test_package)  
            for pack_obj in test_pack_obj:
                package_prices = pack_obj.price
                test_package_price_list.append(package_prices)

            sub_total_package =  sum(test_package_price_list) 
            # print(sub_total_package, "total package price")

        request.data['blood_test_order_no'] = generate_blood_test_order_no()
        if request.data['blood_test']==[] and request.data['test_package']==[]:
            request.data['archived']=True
            
        if request.data['blood_test']!=[] and request.data['test_package']!=[]:
                request.data['total_amount']= sub_total_test + sub_total_package
        if request.data['blood_test']==[] and request.data['test_package']!=[]:
            request.data['total_amount']= sub_total_package

        if request.data['blood_test']!=[]and request.data['test_package']==[]:
             request.data['total_amount']=  sub_total_test

        if request.data['blood_test']== []:
            request.data['is_blood_test']=False
        else:
            request.data['is_blood_test']= True

        if request.data['test_package']== []:
            request.data['is_test_package']=False
        else:
            request.data['is_test_package']=True

        blood_test_order_serializers = SaveBloodTestOrderSerializer(data= request.data, context={'request': request})
      
        if  blood_test_order_serializers.is_valid(raise_exception =True):
            blood_test_order_serializers.save()
        
            return Response( blood_test_order_serializers.data, status=status.HTTP_201_CREATED)
        return Response( blood_test_order_serializers.errors, status=status.HTTP_400_BAD_REQUEST)


    def partial_update(self, request, *args, **kwargs):
        '''
        partial update method for blood test category
        '''
        try:
            remarks = str(request.data['remarks']).strip()
            if len(remarks) <= 0:
                return Response({'remarks': 'Please give at least one word for remarks'},
                                status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'remarks': 'Please Provide remarks'}, status=status.HTTP_400_BAD_REQUEST)
        instance = self.get_object()
        blood_test_price_list= []
        test_package_price_list =[]
        blood_tests=request.data['blood_test']
        test_packages= request.data['test_package']
        for blood_test in blood_tests:
            blood_test_obj= BloodTest.objects.filter(id=blood_test)
            for test_obj in  blood_test_obj:
                prices= test_obj.price
                blood_test_price_list.append(prices)

            sub_total_test = sum(blood_test_price_list)
              
              
        for test_package in test_packages:
            test_pack_obj= TestPackage.objects.filter(id = test_package)  
            for pack_obj in test_pack_obj:
                package_prices =pack_obj.price
                test_package_price_list.append(package_prices)

            sub_total_package =  sum(test_package_price_list) 
            request.data['total_amount']= sub_total_test + sub_total_package

            if request.data['blood_test']== []:
                request.data['is_blood_test']=False
            else:
                request.data['is_blood_test']= True

            if request.data['test_package']== []:
                request.data['is_test_package']=False
            else:
                request.data['is_test_package']=True

        serializer = self.serializer_class(instance, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            '''
            for log history. Atleast one reason must be given if update is made
            '''
            update_change_reason(instance, remarks)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get_queryset(self):
        queryset = super().get_queryset()
        user= self.request.user
        queryset = queryset.filter(archived=False)
        return queryset if user.is_superuser else queryset.filter(created_by=user)



class DeleteBloodTestOrderOrderViewSet(generics.DestroyAPIView):
    queryset = BloodTestOrderMain.objects.all()
    serializer_class= DeleteBloodTestOrderSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        print(instance, " this is instance")
        instance.archived=True
        # print(instance, " this is instance")
        instance.save()
        queryset=BloodTestOrderMain.objects.filter(archived=False)
        serializer = DeleteBloodTestOrderSerializer(queryset,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuickUpdateBloodOrderViewSet(viewsets.ModelViewSet):
    permission_classes = [QuickUpdateBloodTestOrderOrderPermission]
    serializer_class =  QuickUpdateBloodTestOrderSerializer
    queryset =BloodTestOrderMain.objects.all()
    http_method_names = ['patch',]

    @transaction.atomic
    @action(detail= True, url_path = "quick-update-blood-order", methods=['PATCH'])
    def patch(self, request, pk):
        instance = BloodTestOrderMain.objects.get(id=pk)

        serializer = QuickUpdateBloodTestOrderSerializer(instance, data = request.data, partial=True, context={'request': request,  'pk': pk})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

