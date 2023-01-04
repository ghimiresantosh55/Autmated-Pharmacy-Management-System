from django.shortcuts import render

from rest_framework import viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
import django_filters
from . serializers import BloodTestCategorySerializer, BloodTestSerializer, TestPackageSerializer
from .models import BloodTestCategory, BloodTest, TestPackage
from  . blood_test_permissions import  BloodTestCategoryPermission, BloodTestPermission, TestPackagePermission
from simple_history.utils import update_change_reason
from rest_framework.response import Response


class FilterForBloodTestCategory(django_filters.FilterSet):
    '''
    custom filter for BloodTestCategory
    '''
    date = django_filters.DateFromToRangeFilter(field_name="created_date_ad")
    name = django_filters.CharFilter(field_name="name", lookup_expr='iexact')
   
    class Meta:
        model = BloodTestCategory
        fields = ['name', ]


class FilterForBloodTest(django_filters.FilterSet):
    '''
    custom filter for BloodTest
    '''
    date = django_filters.DateFromToRangeFilter(field_name="created_date_ad")
    name = django_filters.CharFilter(field_name="name", lookup_expr='iexact')
   
    class Meta:
        model = BloodTest
        fields = ['name', ]


class FilterForTestPackage(django_filters.FilterSet):
    '''
    custom filter for TestPackage
    '''
    date = django_filters.DateFromToRangeFilter(field_name="created_date_ad")
    name = django_filters.CharFilter(field_name="name", lookup_expr='iexact')
   
    class Meta:
        model = TestPackage
        fields = ['name', ]



class BloodTestCategoryViewSet(viewsets.ModelViewSet):
    '''
    Readonly model viewset for Blood Test Category
    '''
    permission_classes = [BloodTestCategoryPermission]
    queryset = BloodTestCategory.objects.all().order_by('id')
    serializer_class = BloodTestCategorySerializer
    filter_class =  FilterForBloodTestCategory
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ['name', 'id']
    ordering_fields = ['name', ]

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
        serializer = self.serializer_class(instance, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            '''
            for log history. Atleast one reason must be given if update is made
            '''
            update_change_reason(instance, remarks)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class BloodTestViewSet(viewsets.ModelViewSet):
    '''
    Readonly model viewset for Blood Test
    '''
    permission_classes = [BloodTestPermission]
    queryset = BloodTest.objects.all().order_by('id')
    serializer_class = BloodTestSerializer
    filter_class =  FilterForBloodTest
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ['name', 'id']
    ordering_fields = ['name', ]

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
        serializer = self.serializer_class(instance, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            '''
            for log history. Atleast one reason must be given if update is made
            '''
            update_change_reason(instance, remarks)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class TestPackageViewSet(viewsets.ModelViewSet):
    '''
    Readonly model viewset for Blood Test
    '''
    permission_classes = [TestPackagePermission]
    queryset = TestPackage.objects.all().order_by('id')
    serializer_class = TestPackageSerializer
    filter_class =  FilterForTestPackage
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ['name', 'id']
    ordering_fields = ['name', ]

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
        serializer = self.serializer_class(instance, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            '''
            for log history. Atleast one reason must be given if update is made
            '''
            update_change_reason(instance, remarks)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)