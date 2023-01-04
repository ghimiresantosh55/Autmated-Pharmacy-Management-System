'''
function for generate customer order no.
'''
from .models import SaleMain
from src.custom_lib.functions.fiscal_year import get_fiscal_year_code_bs

ORDER_NO_LENGTH = 7


def generate_sale_no():
    '''
    this function will generate customer order number
    '''
    sale_count = SaleMain.objects.count()
    max_id = str(sale_count + 1)
    fiscal_year_code = get_fiscal_year_code_bs()
    # generating of id like CO-77/78-0000000001 , CO-77/78-0000000002 ..
    unique_id = "SA-" + fiscal_year_code + "-" + max_id.zfill(ORDER_NO_LENGTH)
    return unique_id


