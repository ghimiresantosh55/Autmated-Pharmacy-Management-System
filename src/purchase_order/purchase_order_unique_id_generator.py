from .models import PurchaseOrderMain, PurchaseOrderReceivedMain

from src.custom_lib.functions.fiscal_year import get_fiscal_year_code_bs
# format order_no according to given digits
PURCHASE_ORDER_LENGTH = 7

fiscal_year_code = get_fiscal_year_code_bs()

# generate unique order_no for purchase_order_master
def generate_order_no(purchase_order_type):

    # for Purchase order
    if purchase_order_type == 1:
        cancel_count = PurchaseOrderMain.objects.filter(purchase_order_type=purchase_order_type).count()
        max_id = str(cancel_count + 1)
        # generate id = PO-77/78-0000000001, PO-77/78-0000000002 ...
        #  zfill() method adds zeros (0) at the beginning of the string, until it reaches the specified length
        unique_id = "PO-" + fiscal_year_code + "-" + max_id.zfill(PURCHASE_ORDER_LENGTH)
        return unique_id

    # for Purchase cancelled
    elif purchase_order_type == 2:
        cancel_count = PurchaseOrderMain.objects.filter(purchase_order_type=purchase_order_type).count()
        max_id = str(cancel_count + 1)
        # generate id = PC-77/78-0000000001, PC-77/78-0000000002 ...
        #  zfill() method adds zeros (0) at the beginning of the string, until it reaches the specified length
        unique_id = "PC-" + fiscal_year_code + "-" + max_id.zfill(PURCHASE_ORDER_LENGTH)
        return unique_id

    # for Purchase approved
    elif purchase_order_type == 3:
        cancel_count = PurchaseOrderMain.objects.filter(purchase_order_type=purchase_order_type).count()
        max_id = str(cancel_count + 1)
        # generate id = PA-77/78-0000000001, PA-77/78-0000000002 ...
        #  zfill() method adds zeros (0) at the beginning of the string, until it reaches the specified length
        unique_id = "PA-" + fiscal_year_code + "-" + max_id.zfill(PURCHASE_ORDER_LENGTH)
        return unique_id

    else:
        return ValueError


def generate_purchase_order_received_no(purchase_order_received_type):
    if purchase_order_received_type == 1:
        count = PurchaseOrderReceivedMain.objects.filter(purchase_order_received_type=purchase_order_received_type).count()
        max_id = str(count + 1)
        # generate id = PU-77/78-0000000001, PU-77/78-0000000002 ...
        #  zfill() method adds zeros (0) at the beginning of the string, until it reaches the specified length
        unique_id = "POR-" + fiscal_year_code + "-" + max_id.zfill(PURCHASE_ORDER_LENGTH)
        return unique_id


    elif purchase_order_received_type == 2:
        count = PurchaseOrderReceivedMain.objects.filter( purchase_order_received_type= purchase_order_received_type).count()
        max_id = str(count + 1)
        # generate id = PC-77/78-0000000001, PC-77/78-0000000002 ...
        #  zfill() method adds zeros (0) at the beginning of the string, until it reaches the specified length
        unique_id = "POV-" + fiscal_year_code + "-" + max_id.zfill(PURCHASE_ORDER_LENGTH)
        return unique_id


