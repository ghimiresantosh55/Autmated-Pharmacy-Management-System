
from rest_framework.pagination import PageNumberPagination

from rest_framework import pagination


class CustomPagination(PageNumberPagination):
    '''
    custom page number pagination class
    '''
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10


class CustomPaginationForBrand(PageNumberPagination):
    '''
    custom page number pagination class for brand list
    '''
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 20


class CustomLimitOffsetPagination(pagination.LimitOffsetPagination):
    '''
    custom limit offset pagination class
    '''
    default_limit = 2
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 50