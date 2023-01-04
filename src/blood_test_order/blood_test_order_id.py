from .models import BloodTestOrderMain
from src.custom_lib.functions.fiscal_year import get_fiscal_year_code_bs

BLOOD_TEST_ORDER_NO_LENGTH = 7


def generate_blood_test_order_no():
    '''
    this function will generate BLOOD TEST order number
    '''
    test_order_count = BloodTestOrderMain.objects.count()
    max_id = str( test_order_count + 1)
    fiscal_year_code = get_fiscal_year_code_bs()
    unique_id = "BO-" + fiscal_year_code + "-" + max_id.zfill(BLOOD_TEST_ORDER_NO_LENGTH)
    return unique_id
