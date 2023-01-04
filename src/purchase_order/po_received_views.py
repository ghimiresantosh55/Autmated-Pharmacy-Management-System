
from rest_framework.generics import CreateAPIView
from .po_received_serializer import SaveCustomerOrderReceivedSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .purchase_order_permissions import  PurchaseOrderReceivedPermission

class POReceivedViewSet(CreateAPIView):
    serializer_class = SaveCustomerOrderReceivedSerializer
    permission_classes= [PurchaseOrderReceivedPermission]

    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        # print("hhhhh")
        if serializer.is_valid(raise_exception=True):
            # print(serializer.data,"this is se")
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            # print("hello")
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        