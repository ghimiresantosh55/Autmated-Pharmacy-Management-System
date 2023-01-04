'''
View for tenant
'''
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.db import connection
from .models import Tenant
from .serializer import TenantSerializer

class TenantMapView(APIView):
    '''
    Api view for tenant mapview
    '''
    permission_classes = [AllowAny]

    def get(self, request):
        '''
        Function for get tenant
        '''
        connection.cursor().execute("SET search_path to public")
        tenant_map = Tenant.objects.all()
        tenant_serializer = TenantSerializer(tenant_map, many=True)

        # tenants_map = [{
        #     'id': 1,
        #     'sub_domain_address': 'customer1.pims-backend.staging.merakitechs.com',
        #     'branch_name': 'customer1',
        # },
        # {
        #     'id': 2,
        #     'sub_domain_address': 'customer2.pims-backend.staging.merakitechs.com',
        #     'branch_name': 'customer2',
        # }]
        return Response(tenant_serializer.data, status=status.HTTP_200_OK)
