from typing import List
from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from src.purchase.models import PurchaseDetail

from src.store.models import Location
from .serializers import LocationListSerializer, LocationUpdateSerializer
from rest_framework import status
# Create your views here.


class LocationListApiView(ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationListSerializer



class LocationUpdateApiView(CreateAPIView):
    queryset = PurchaseDetail.objects.all()
    serializer_class = LocationUpdateSerializer


    def create(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "successfully updated"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LocationCheckApiView(CreateAPIView):
    queryset = PurchaseDetail.objects.all()
    serializer_class = LocationUpdateSerializer


    def create(self, request, *args, **kwargs):
        try: 
            purchase_detail_id = request.data['purchase_detail_id']
            location_id  = request.data['location_id']
            purchase_detail = PurchaseDetail.objects.get(id=purchase_detail_id)
            location = purchase_detail.location
            

            if(int(purchase_detail_id) == int(purchase_detail.id)) and (int(location.id) == int(location_id)):
                return Response({"message": "success"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Invalid location or purchase detail id"}, status=status.HTTP_400_BAD_REQUEST)

        except KeyError:
            return Response({"message": "please provide purchase detail id and location id"}, status=status.HTTP_400_BAD_REQUEST)
