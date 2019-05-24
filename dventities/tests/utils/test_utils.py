from django.test import TestCase

from dventities.models import *
from dventities.util.util import *
#print(dir(dventities.util) )
print(dir())

        
class UtilTests(TestCase):

    def test_stage_table_create(self):
        table_def = """
Table "GDELT_HANA.STAGE_JDE_GL_TRANSACTION_MASTER_SKINNY"
Column Name,Type,Length,Nullable,Keypos
"ACCOUNT_NUMBER","VARCHAR","30","YES","n/a"
"DOCUMENT_COMPANY","VARCHAR","10","YES","n/a"
"GL_DOC_TYPE","VARCHAR","4","YES","n/a"
"GL_DOC_NUMBER","INTEGER","10","YES","n/a"
"GL_DATE","DATE","10","NO","n/a"
"JE_LINE_NUMBER","DECIMAL","22,1","YES","n/a"
"GL_POSTED_CODE","VARCHAR","2","YES","n/a"
"BATCH_NUMBER","INTEGER","10","YES","n/a"
"BATCH_TYPE","VARCHAR","4","YES","n/a"
"BATCH_DATE","DATE","10","YES","n/a"
"COMPANY","VARCHAR","10","YES","n/a"
"BUSINESS_UNIT","VARCHAR","24","YES","n/a"
"SUBLEDGER","VARCHAR","16","YES","n/a"
"SUBLEDGER_TYPE","VARCHAR","2","YES","n/a"
"LEDGER_TYPE","VARCHAR","4","YES","n/a"
"CURRENCY_CODE","VARCHAR","6","YES","n/a"
"EXCHANGE_RATE","DECIMAL","22,7","YES","n/a"
"HISTORICAL_EXCHANGE_RATE","DECIMAL","22,7","YES","n/a"
"AMOUNT","DECIMAL","22,3","YES","n/a"
"ADDRESS_NUMBER","INTEGER","10","YES","n/a"
"INVOICE_NUMBER","VARCHAR","50","YES","n/a"
"INVOICE_DATE","DATE","10","YES","n/a"
"PO_NUMBER","VARCHAR","16","YES","n/a"
"ORDER_TYPE","VARCHAR","4","YES","n/a"
"LINE_NUMBER","DECIMAL","22,3","YES","n/a"
"LINE_EXTENSION_CODE_2","VARCHAR","4","YES","n/a"
"SERIAL_NUMBER","VARCHAR","50","YES","n/a"
"DOCUMENT_ORIGINAL","INTEGER","10","YES","n/a"
"DOCUMENT_COMPANY_ORIGINAL","VARCHAR","10","YES","n/a"
"DOCUMENT_TYPE_ORIGINAL","VARCHAR","4","YES","n/a"
"ITEM_ID","INTEGER","10","YES","n/a"
"PROGRAM_ID","VARCHAR","20","YES","n/a"
"USER_ID","VARCHAR","20","YES","n/a"
"DATE_UPDATED","DATE","10","YES","n/a"
"FLAG","INTEGER","10","YES","n/a"

     
        """
        create_stage_table_from_hdbsql_output(table_def)

