'''
function for generate customer order no.
'''
from .models import OrderMain
from src.custom_lib.functions.fiscal_year import get_fiscal_year_code_bs

ORDER_NO_LENGTH = 7


def generate_customer_order_no():
    '''
    this function will generate customer order number
    '''
    order_count = OrderMain.objects.count()
    max_id = str(order_count + 1)
    fiscal_year_code = get_fiscal_year_code_bs()
    # generating of id like CO-77/78-0000000001 , CO-77/78-0000000002 ..
    unique_id = "CO-" + fiscal_year_code + "-" + max_id.zfill(ORDER_NO_LENGTH)
    return unique_id


