from src.custom_lib.functions.fiscal_year import get_fiscal_year_code_bs
from src.purchase_order.models import PurchaseOrderMain
ORDER_NO_LENGTH = 7


def generate_purchase_order_no():
    order_count = PurchaseOrderMain.objects.count()
    max_id = str(order_count + 1)
    fiscal_year_code = get_fiscal_year_code_bs()
    # generating of id like CO-77/78-0000000001 , CO-77/78-0000000002 ..
    unique_id = "PO-" + fiscal_year_code + "-" + max_id.zfill(ORDER_NO_LENGTH)
    return unique_id