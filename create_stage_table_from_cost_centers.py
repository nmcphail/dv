from django.core.exceptions import ObjectDoesNotExist

import pprint

from dventities.models import *
from dventities.util.util import *


from codegen.exceptions import CodeGenerationError
from codegen.stage_table.stage_table_code_generation import *

from codegen.hub import hub_table
from codegen.manager import manager



# Table def is created from a command like:

# hdbsql -n anvhanasb01 -i 90 -d HXE -u gdelt_hana
#   -p xxxxxx \dc GDELT_HANA.STAGE_JDE%GL_TRANSACTION_MASTER%SKINNY

table_def = """
Table "GDELT_HANA.JDE_COST_CENTER_MASTERS"
Column Name,Type,Length,Nullable,Keypos
"COMPANY","VARCHAR","10","YES","n/a"
"BUSINESS_UNIT","VARCHAR","24","YES","n/a"
"ADDRESS_NUMBER","INTEGER","10","YES","n/a"
"BUSINESS_UNIT_TYPE","VARCHAR","4","YES","n/a"
"DESCRIPTION_COMP","VARCHAR","80","YES","n/a"
"LEVEL_OF_DETAIL","VARCHAR","2","YES","n/a"
"MODEL_ACCOUNT_CONS","VARCHAR","2","YES","n/a"
"DESCRIPTION","VARCHAR","120","YES","n/a"
"DIVISION","VARCHAR","60","YES","n/a"
"SUB_DIVISION","VARCHAR","60","YES","n/a"
"MARKET_SEGMENT","VARCHAR","6","YES","n/a"
"MARKET_APPLICATION","VARCHAR","6","YES","n/a"
"PRODUCT_GROUP","VARCHAR","6","YES","n/a"
"PRODUCT_FAMILY","VARCHAR","6","YES","n/a"
"PRODUCT_CODE","VARCHAR","6","YES","n/a"
"BRAND","VARCHAR","6","YES","n/a"
"PROJECT","VARCHAR","6","YES","n/a"
"PLATFORM","VARCHAR","6","YES","n/a"
"PLANT","VARCHAR","6","YES","n/a"
"CC_TYPE","VARCHAR","6","YES","n/a"
"SUB_TYPE","VARCHAR","6","YES","n/a"
"COUNTRY","VARCHAR","6","YES","n/a"
"COUNTRY_LOCATION","VARCHAR","6","YES","n/a"
"CATEGORY_CODE_16","VARCHAR","6","YES","n/a"
"CATEGORY_CODE_17","VARCHAR","6","YES","n/a"
"CATEGORY_CODE_18","VARCHAR","6","YES","n/a"
"LOCAL_1","VARCHAR","6","YES","n/a"
"LOCAL_2","VARCHAR","6","YES","n/a"
"ENTERPRISE_PROJECT_NUMBER","VARCHAR","20","YES","n/a"
"CATEGORY_CODE_22","VARCHAR","20","YES","n/a"
"CATEGORY_CODE_23","VARCHAR","20","YES","n/a"
"CATEGORY_CODE_24","VARCHAR","20","YES","n/a"
"CATEGORY_CODE_25","VARCHAR","20","YES","n/a"
"CATEGORY_CODE_26","VARCHAR","20","YES","n/a"
"CATEGORY_CODE_27","VARCHAR","20","YES","n/a"
"CATEGORY_CODE_28","VARCHAR","20","YES","n/a"
"CATEGORY_CODE_29","VARCHAR","20","YES","n/a"
"CATEGORY_CODE_30","VARCHAR","20","YES","n/a"
"POSTING_EDIT","VARCHAR","2","YES","n/a"
"PROJECT_NUMBER","VARCHAR","24","YES","n/a"
"APS_BUSINESS_UNIT","VARCHAR","2","YES","n/a"
"BRANCH_TYPE","VARCHAR","30","YES","n/a"
"TARGET_BUSINESS_UNIT","VARCHAR","24","YES","n/a"
"WORK_STATION_ID","VARCHAR","20","YES","n/a"
"PROGRAM_ID","VARCHAR","20","YES","n/a"
"USER_ID","VARCHAR","20","YES","n/a"
"DATE_UPDATED","DATE","10","YES","n/a"
"ADDRESS_NUMBER_JOB_AR","INTEGER","10","YES","n/a"
"ALLOCATION_LEVEL","VARCHAR","4","YES","n/a"
"ALLOCATION_SUMM_METHOD","VARCHAR","2","YES","n/a"
"AMOUNT_COST_AT_COMPLETION","DECIMAL","22,2","YES","n/a"
"AMOUNT_COST_TO_COMP_OBSOLETE","DECIMAL","22,2","YES","n/a"
"AMOUNT_PROFIT_AT_COMPLETION","DECIMAL","22,2","YES","n/a"
"BILLING_TYPE_BUSINESS_UNIT","VARCHAR","2","YES","n/a"
"BUSINESS_UNIT_SUBSEQUENT","VARCHAR","24","YES","n/a"
"CERTIFIED_JOB","VARCHAR","2","YES","n/a"
"CONTRACT_TYPE","VARCHAR","8","YES","n/a"
"COUNTY","VARCHAR","6","YES","n/a"
"DATE_ACTUAL_COMPLETE","DATE","10","YES","n/a"
"DATE_ACTUAL_START","DATE","10","YES","n/a"
"DATE_FINAL_PAYMENT_JULIAN","DATE","10","YES","n/a"
"DATE_OTHER_5","DATE","10","YES","n/a"
"DATE_OTHER_6","DATE","10","YES","n/a"
"DATE_PLANNED_COMPLETE","DATE","10","YES","n/a"
"DATE_PLANNED_START","DATE","10","YES","n/a"
"DESCRIPTION_2","VARCHAR","60","YES","n/a"
"DESCRIPTION_3","VARCHAR","60","YES","n/a"
"DESCRIPTION_4","VARCHAR","60","YES","n/a"
"EQUAL_EMPLOYMENT_OPPORTUNITY","VARCHAR","2","YES","n/a"
"EQUIPMENT_RATE_CODE","VARCHAR","4","YES","n/a"
"GL_BANK_ACCOUNT","VARCHAR","16","YES","n/a"
"INTEREST_COMP_LATE_REVENUE","VARCHAR","8","YES","n/a"
"INTEREST_COMPUTATION_CODE_AR","VARCHAR","8","YES","n/a"
"INVOICE_STMT_SUMM_METHOD","VARCHAR","2","YES","n/a"
"LABOR_DISTRIBUTION_METHOD","VARCHAR","2","YES","n/a"
"LABOR_DISTRIBUTION_MULTIPLIER","DECIMAL","22,4","YES","n/a"
"OBJECT_ACCOUNT_BURDEN","VARCHAR","12","YES","n/a"
"OBJECT_ACCOUNT_LABOR_ACCOUNT","VARCHAR","12","YES","n/a"
"OBJECT_ACCOUNT_PREMIUM_ACCOUNT","VARCHAR","12","YES","n/a"
"PERCENT_COMPLETE","INTEGER","10","YES","n/a"
"PERCENT_COMPLETE_AGGR_DETAIL","DECIMAL","22,2","YES","n/a"
"STATE","VARCHAR","6","YES","n/a"
"SUBLEDGER_INACTIVE_CODE","VARCHAR","2","YES","n/a"
"SUBSIDIARY_BURDEN_COST_CODE","VARCHAR","16","YES","n/a"
"SUPERVISOR","INTEGER","10","YES","n/a"
"TAX_AREA","VARCHAR","20","YES","n/a"
"TAX_DEDUCTION_CODES_1","VARCHAR","8","YES","n/a"
"TAX_DEDUCTION_CODES_2","VARCHAR","8","YES","n/a"
"TAX_DEDUCTION_CODES_3","VARCHAR","8","YES","n/a"
"TAX_DEDUCTION_CODES_4","VARCHAR","8","YES","n/a"
"TAX_DEDUCTION_CODES_5","VARCHAR","8","YES","n/a"
"TAX_DEDUCTION_CODES_6","VARCHAR","8","YES","n/a"
"TAX_DEDUCTION_CODES_7","VARCHAR","8","YES","n/a"
"TAX_DEDUCTION_CODES_8","VARCHAR","8","YES","n/a"
"TAX_DEDUCTION_CODES_9","VARCHAR","8","YES","n/a"
"TAX_DEDUCTION_CODES_10","VARCHAR","8","YES","n/a"
"TAX_DISTRIBUTABLE_1","VARCHAR","2","YES","n/a"
"TAX_DISTRIBUTABLE_2","VARCHAR","2","YES","n/a"
"TAX_DISTRIBUTABLE_3","VARCHAR","2","YES","n/a"
"TAX_DISTRIBUTABLE_4","VARCHAR","2","YES","n/a"
"TAX_DISTRIBUTABLE_5","VARCHAR","2","YES","n/a"
"TAX_DISTRIBUTABLE_6","VARCHAR","2","YES","n/a"
"TAX_DISTRIBUTABLE_7","VARCHAR","2","YES","n/a"
"TAX_DISTRIBUTABLE_8","VARCHAR","2","YES","n/a"
"TAX_DISTRIBUTABLE_9","VARCHAR","2","YES","n/a"
"TAX_DISTRIBUTABLE_10","VARCHAR","2","YES","n/a"
"TAX_ENTITY","INTEGER","10","YES","n/a"
"TAX_EXPL_CODE","VARCHAR","4","YES","n/a"
"TAX_OR_DEDUCTION_COMP_STS_1","VARCHAR","2","YES","n/a"
"TAX_OR_DEDUCTION_COMP_STS_2","VARCHAR","2","YES","n/a"
"TAX_OR_DEDUCTION_COMP_STS_3","VARCHAR","2","YES","n/a"
"TAX_OR_DEDUCTION_COMP_STS_4","VARCHAR","2","YES","n/a"
"TAX_OR_DEDUCTION_COMP_STS_5","VARCHAR","2","YES","n/a"
"TAX_OR_DEDUCTION_COMP_STS_6","VARCHAR","2","YES","n/a"
"TAX_OR_DEDUCTION_COMP_STS_7","VARCHAR","2","YES","n/a"
"TAX_OR_DEDUCTION_COMP_STS_8","VARCHAR","2","YES","n/a"
"TAX_OR_DEDUCTION_COMP_STS_9","VARCHAR","2","YES","n/a"
"TAX_OR_DEDUCTION_COMP_STS_10","VARCHAR","2","YES","n/a"
"TAX_RATE_AREA","VARCHAR","20","YES","n/a"
"UNITS_TOTAL","DECIMAL","22,2","YES","n/a"
"CATEGORY_CODE_31","VARCHAR","20","YES","n/a"
"CATEGORY_CODE_32","VARCHAR","20","YES","n/a"
"CATEGORY_CODE_33","VARCHAR","20","YES","n/a"
"CATEGORY_CODE_34","VARCHAR","20","YES","n/a"
"CATEGORY_CODE_35","VARCHAR","20","YES","n/a"
"CATEGORY_CODE_36","VARCHAR","20","YES","n/a"
"CATEGORY_CODE_37","VARCHAR","20","YES","n/a"
"CATEGORY_CODE_38","VARCHAR","20","YES","n/a"
"CATEGORY_CODE_39","VARCHAR","20","YES","n/a"
"CATEGORY_CODE_40","VARCHAR","20","YES","n/a"
"CATEGORY_CODE_41","VARCHAR","20","YES","n/a"
"CATEGORY_CODE_42","VARCHAR","20","YES","n/a"
"CATEGORY_CODE_43","VARCHAR","20","YES","n/a"
"CATEGORY_CODE_44","VARCHAR","20","YES","n/a"
"CATEGORY_CODE_45","VARCHAR","20","YES","n/a"
"CATEGORY_CODE_46","VARCHAR","20","YES","n/a"
"CATEGORY_CODE_47","VARCHAR","20","YES","n/a"
"CATEGORY_CODE_48","VARCHAR","20","YES","n/a"
"CATEGORY_CODE_49","VARCHAR","20","YES","n/a"
"CATEGORY_CODE_50","VARCHAR","20","YES","n/a"
"ADDRESS_NUMBER_1","INTEGER","10","YES","n/a"
"ADDRESS_NUMBER_2","INTEGER","10","YES","n/a"
"ADDRESS_NUMBER_3","INTEGER","10","YES","n/a"
"ADDRESS_NUMBER_4","INTEGER","10","YES","n/a"
"ADDRESS_NUMBER_5","INTEGER","10","YES","n/a"
"RELATED_BUSINESS_UNIT","VARCHAR","24","YES","n/a"
"ORDER_NUMBER","INTEGER","10","YES","n/a"
"PARENT_CONTROL_NUMBER","INTEGER","10","YES","n/a"
"CONTRACT_LEVEL_NUMBER","INTEGER","10","YES","n/a"
"BURDEN_CATEGORY","VARCHAR","10","YES","n/a"
"ADJUSTMENT_ENTRY","VARCHAR","2","YES","n/a"
"UNALLOWABLE_FLAG","VARCHAR","2","YES","n/a"
"""
stage_table = create_stage_table_from_hdbsql_output(table_def)
cost_center = Hub.objects.get(name='Cost Center')
company = Hub.objects.get(name='Company')

cost_center_loader = stage_table.get_hub_loader_for_hub(cost_center)
if cost_center_loader is None:
    cost_center_loader = HubLoader(stage_table=stage_table, hub=cost_center)
    cost_center_loader.clean()
    cost_center_loader.save()
    
#company = Hub.objects.get(name='Company')
#company_loader = stage_table.get_hub_loader_for_hub(company)
#if company_loader is None:
#    company_loader = HubLoader(stage_table=stage_table, hub=company)
#    company_loader.clean()
#    company_loader.save()


#addresses = cost_center.find_or_create_hub_satelite( 'addresses')
#addresses_loader = cost_center_loader.find_or_create_hub_satelite_loader( addresses)

#tax_codes = cost_center.find_or_create_hub_satelite( 'e1_tax_codes')
#tax_codes_loader = cost_center_loader.find_or_create_hub_satelite_loader(tax_codes)

    
#if addresses is None:
    
f = stage_table.stagetablefield_set.get(field_name='BUSINESS_UNIT')
f.stage_table_primary_key = True
f.clean()
f.save()


hlf = cost_center_loader.get_field_by_name('BUSINESS_UNIT')
if hlf is None:
    hlf = HubLoaderField(hub_loader = cost_center_loader, hub_field_name='Cost Center')
    hlf.stage_table_field = f
    hlf.clean()
    hlf.save()


stage_table.add_stage_table_field_to_hub_loader('COMPANY', 'Company', 'Company')

#f = stage_table.stagetablefield_set.get(field_name='COMPANY')
#hlf = company_loader.get_field_by_name('COMPANY')
#if hlf is None:
#    hlf = HubLoaderField(hub_loader = company_loader, hub_field_name='Company')
#    hlf.stage_table_field = f
#    hlf.clean()
#    hlf.save()

stage_table.add_link_loader_for_hub_names('Cost Center Company', ( ('Cost Center', True), ('Company', False)))    
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Core Attributes', 'COMPANY')

    
#f=addresses_loader.add_field('ADDRESS_NUMBER', True )
#f=addresses_loader.add_field('ADDRESS_NUMBER_1', True )
#f=addresses_loader.add_field('ADDRESS_NUMBER_2', True )
#f=addresses_loader.add_field('ADDRESS_NUMBER_3', True )
#f=addresses_loader.add_field('ADDRESS_NUMBER_4', True )
#f=addresses_loader.add_field('ADDRESS_NUMBER_5', True )

#f=tax_codes_loader.add_field('TAX_DEDUCTION_CODES_1', True)
#f=tax_codes_loader.add_field('TAX_DEDUCTION_CODES_2', True)
#f=tax_codes_loader.add_field('TAX_DEDUCTION_CODES_3', True)
#f=tax_codes_loader.add_field('TAX_DEDUCTION_CODES_4', True)
#f=tax_codes_loader.add_field('TAX_DEDUCTION_CODES_5', True)
#f=tax_codes_loader.add_field('TAX_DEDUCTION_CODES_6', True)
#f=tax_codes_loader.add_field('TAX_DEDUCTION_CODES_7', True)
#f=tax_codes_loader.add_field('TAX_DEDUCTION_CODES_8', True)
#f=tax_codes_loader.add_field('TAX_DEDUCTION_CODES_9', True)
#f=tax_codes_loader.add_field('TAX_DEDUCTION_CODES_10', True)
#f=tax_codes_loader.add_field('TAX_DISTRIBUTABLE_1', True)
#f=tax_codes_loader.add_field('TAX_DISTRIBUTABLE_2', True)
#f=tax_codes_loader.add_field('TAX_DISTRIBUTABLE_3', True)
#f=tax_codes_loader.add_field('TAX_DISTRIBUTABLE_4', True)
#f=tax_codes_loader.add_field('TAX_DISTRIBUTABLE_5', True)
#f=tax_codes_loader.add_field('TAX_DISTRIBUTABLE_6', True)
#f=tax_codes_loader.add_field('TAX_DISTRIBUTABLE_7', True)
#f=tax_codes_loader.add_field('TAX_DISTRIBUTABLE_8', True)
#f=tax_codes_loader.add_field('TAX_DISTRIBUTABLE_9', True)
#f=tax_codes_loader.add_field('TAX_DISTRIBUTABLE_10', True)
#f=tax_codes_loader.add_field('TAX_ENTITY', True)
#f=tax_codes_loader.add_field('TAX_EXPL_CODE', True)
#f=tax_codes_loader.add_field('TAX_OR_DEDUCTION_COMP_STS_1', True)
#f=tax_codes_loader.add_field('TAX_OR_DEDUCTION_COMP_STS_2', True)
#f=tax_codes_loader.add_field('TAX_OR_DEDUCTION_COMP_STS_3', True)
#f=tax_codes_loader.add_field('TAX_OR_DEDUCTION_COMP_STS_4', True)
#f=tax_codes_loader.add_field('TAX_OR_DEDUCTION_COMP_STS_5', True)
#f=tax_codes_loader.add_field('TAX_OR_DEDUCTION_COMP_STS_6', True)
#f=tax_codes_loader.add_field('TAX_OR_DEDUCTION_COMP_STS_7', True)
#f=tax_codes_loader.add_field('TAX_OR_DEDUCTION_COMP_STS_8', True)
#f=tax_codes_loader.add_field('TAX_OR_DEDUCTION_COMP_STS_9', True)
#f=tax_codes_loader.add_field('TAX_OR_DEDUCTION_COMP_STS_10', True)
#f=tax_codes_loader.add_field('TAX_RATE_AREA', True)



stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Descriptions','DESCRIPTION')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Descriptions','DESCRIPTION_COMP')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Descriptions','DESCRIPTION_2')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Descriptions','DESCRIPTION_3')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Descriptions','DESCRIPTION_4')


stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Addresses','ADDRESS_NUMBER_1')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Addresses','ADDRESS_NUMBER_2')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Addresses','ADDRESS_NUMBER_3')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Addresses','ADDRESS_NUMBER_4')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Addresses','ADDRESS_NUMBER_5')


stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Core Attributes','DIVISION')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Core Attributes','SUB_DIVISION')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Core Attributes','MARKET_SEGMENT')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Core Attributes','MARKET_APPLICATION')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Core Attributes','PRODUCT_GROUP')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Core Attributes','PRODUCT_FAMILY')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Core Attributes','PRODUCT_CODE')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Core Attributes','BRAND')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Core Attributes','PROJECT')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Core Attributes','PLATFORM')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Core Attributes','PLANT')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Core Attributes','CC_TYPE')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Core Attributes','SUB_TYPE')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Core Attributes','COUNTRY')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Core Attributes','COUNTRY_LOCATION')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Core Attributes','BUSINESS_UNIT_TYPE')


stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Category Codes','CATEGORY_CODE_16')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Category Codes','CATEGORY_CODE_17')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Category Codes','CATEGORY_CODE_18')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Category Codes','CATEGORY_CODE_22')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Category Codes','CATEGORY_CODE_23')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Category Codes','CATEGORY_CODE_24')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Category Codes','CATEGORY_CODE_25')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Category Codes','CATEGORY_CODE_26')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Category Codes','CATEGORY_CODE_27')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Category Codes','CATEGORY_CODE_28')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Category Codes','CATEGORY_CODE_29')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Category Codes','CATEGORY_CODE_30')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Category Codes','CATEGORY_CODE_31')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Category Codes','CATEGORY_CODE_32')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Category Codes','CATEGORY_CODE_33')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Category Codes','CATEGORY_CODE_34')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Category Codes','CATEGORY_CODE_35')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Category Codes','CATEGORY_CODE_36')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Category Codes','CATEGORY_CODE_37')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Category Codes','CATEGORY_CODE_38')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Category Codes','CATEGORY_CODE_39')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Category Codes','CATEGORY_CODE_40')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Category Codes','CATEGORY_CODE_41')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Category Codes','CATEGORY_CODE_42')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Category Codes','CATEGORY_CODE_43')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Category Codes','CATEGORY_CODE_44')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Category Codes','CATEGORY_CODE_45')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Category Codes','CATEGORY_CODE_46')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Category Codes','CATEGORY_CODE_47')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Category Codes','CATEGORY_CODE_48')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Category Codes','CATEGORY_CODE_49')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Category Codes','CATEGORY_CODE_50')



stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Record Information','WORK_STATION_ID')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Record Information','PROGRAM_ID')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Record Information','USER_ID')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Record Information','DATE_UPDATED')

stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Dates','DATE_ACTUAL_COMPLETE')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Dates','DATE_ACTUAL_START')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Dates','DATE_FINAL_PAYMENT_JULIAN')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Dates','DATE_OTHER_5')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Dates','DATE_OTHER_6')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Dates','DATE_PLANNED_COMPLETE')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Dates','DATE_PLANNED_START')


stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Tax Information','TAX_AREA')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Tax Information','TAX_DEDUCTION_CODES_1')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Tax Information','TAX_DEDUCTION_CODES_2')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Tax Information','TAX_DEDUCTION_CODES_3')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Tax Information','TAX_DEDUCTION_CODES_4')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Tax Information','TAX_DEDUCTION_CODES_5')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Tax Information','TAX_DEDUCTION_CODES_6')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Tax Information','TAX_DEDUCTION_CODES_7')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Tax Information','TAX_DEDUCTION_CODES_8')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Tax Information','TAX_DEDUCTION_CODES_9')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Tax Information','TAX_DEDUCTION_CODES_10')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Tax Information','TAX_DISTRIBUTABLE_1')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Tax Information','TAX_DISTRIBUTABLE_2')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Tax Information','TAX_DISTRIBUTABLE_3')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Tax Information','TAX_DISTRIBUTABLE_4')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Tax Information','TAX_DISTRIBUTABLE_5')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Tax Information','TAX_DISTRIBUTABLE_6')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Tax Information','TAX_DISTRIBUTABLE_7')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Tax Information','TAX_DISTRIBUTABLE_8')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Tax Information','TAX_DISTRIBUTABLE_9')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Tax Information','TAX_DISTRIBUTABLE_10')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Tax Information','TAX_ENTITY')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Tax Information','TAX_EXPL_CODE')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Tax Information','TAX_OR_DEDUCTION_COMP_STS_1')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Tax Information','TAX_OR_DEDUCTION_COMP_STS_2')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Tax Information','TAX_OR_DEDUCTION_COMP_STS_3')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Tax Information','TAX_OR_DEDUCTION_COMP_STS_4')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Tax Information','TAX_OR_DEDUCTION_COMP_STS_5')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Tax Information','TAX_OR_DEDUCTION_COMP_STS_6')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Tax Information','TAX_OR_DEDUCTION_COMP_STS_7')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Tax Information','TAX_OR_DEDUCTION_COMP_STS_8')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Tax Information','TAX_OR_DEDUCTION_COMP_STS_9')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Tax Information','TAX_OR_DEDUCTION_COMP_STS_10')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Tax Information','TAX_RATE_AREA')


stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Other','ALLOCATION_LEVEL')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Other','ALLOCATION_SUMM_METHOD')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Other','AMOUNT_COST_AT_COMPLETION')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Other','AMOUNT_COST_TO_COMP_OBSOLETE')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Other','AMOUNT_PROFIT_AT_COMPLETION')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Other','BILLING_TYPE_BUSINESS_UNIT')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Other','BUSINESS_UNIT_SUBSEQUENT')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Other','CERTIFIED_JOB')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Other','CONTRACT_TYPE')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Other','COUNTY')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Other','EQUAL_EMPLOYMENT_OPPORTUNITY')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Other','EQUIPMENT_RATE_CODE')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Other','GL_BANK_ACCOUNT')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Other','INTEREST_COMP_LATE_REVENUE')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Other','INTEREST_COMPUTATION_CODE_AR')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Other','INVOICE_STMT_SUMM_METHOD')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Other','LABOR_DISTRIBUTION_METHOD')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Other','LABOR_DISTRIBUTION_MULTIPLIER')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Other','OBJECT_ACCOUNT_BURDEN')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Other','OBJECT_ACCOUNT_LABOR_ACCOUNT')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Other','OBJECT_ACCOUNT_PREMIUM_ACCOUNT')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Other','PERCENT_COMPLETE')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Other','PERCENT_COMPLETE_AGGR_DETAIL')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Other','STATE')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Other','SUBLEDGER_INACTIVE_CODE')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Other','SUBSIDIARY_BURDEN_COST_CODE')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Other','SUPERVISOR')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Other','UNITS_TOTAL')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Other','RELATED_BUSINESS_UNIT')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Other','ORDER_NUMBER')



stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Other','LOCAL_1')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Other','LOCAL_2')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Other','ENTERPRISE_PROJECT_NUMBER')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Other','POSTING_EDIT')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Other','PROJECT_NUMBER')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Other','APS_BUSINESS_UNIT')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Other','BRANCH_TYPE')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Other','TARGET_BUSINESS_UNIT')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Other','ADDRESS_NUMBER_JOB_AR')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Other','PARENT_CONTROL_NUMBER')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Other','CONTRACT_LEVEL_NUMBER')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Other','BURDEN_CATEGORY')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Other','ADJUSTMENT_ENTRY')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Other','UNALLOWABLE_FLAG')

stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Other','LEVEL_OF_DETAIL')
stage_table.add_hub_satelite_field_for_hub_and_satelite('Cost Center', '', 'E1 Other','MODEL_ACCOUNT_CONS')




    
mm = manager.ModelManager()
stm = manager.StageTableManager(stage_table, mm.artifact_location)
stm.generate_code()


hm = manager.HubManager(cost_center, mm.artifact_location)
hm.generate_code()

hm = manager.HubManager(company, mm.artifact_location)
hm.generate_code()

manager.LinkManager(Link.objects.get(name='Cost Center Company'), mm.artifact_location).generate_code()

#for f in stage_table.stagetablefield_set.all():
#    print(f.field_name)
#    print()
#    print()
#    pprint.pprint(f.get_usage_summary())
#    print()
#    print()

#hs = HubSatelite()
#hs.name = 'addresses'
#hs.hub = hub
#hs.save()
#hs.clean()



