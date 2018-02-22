"""
Module: entities.payees
Representation of a "payee" record, including transformation functions
and support functions for conversion into different formats.

Support functions are built to handle arrays of payees (as opposed to
an individual payee)
"""
from translator.util import digits_only, uppercase, rjust_zero
from translator.util import xform_entity, fire_entity, transform_dict
"""
_PAYEE_TRANSFORMS
-----------------------
Stores metadata associated with each field in a Transmitter record.
Values in key-value pairs represent metadata in the following format:

(default value, length, fill character, transformation function)
"""
_PAYEE_TRANSFORMS_ARR = [
    ("record_type","B",1,"\x00",lambda x: (x)),
    ("payment_year","",4,"\x00",lambda x: (x)),
    ("corrected_return_indicator","",1,"\x00",lambda x: uppercase(x)),
    ("payees_name_control","",4,"\x00",lambda x: uppercase(x)),
    ("type_of_tin","1",1,"\x00",lambda x: (x)),
    ("payees_tin","000000000",9,"\x00",lambda x: digits_only(x)),
    ("payers_account_number_for_payee","",20,"\x00",lambda x: (x)),
    ("payers_office_code","",4,"\x00",lambda x: (x)),
    ("blank_1","",10,"\x00",lambda x: (x)),
    ("payment_amount_1","000000000000",12,"\x00",lambda x: rjust_zero(x,12)),
    ("payment_amount_2","000000000000",12,"\x00",lambda x: rjust_zero(x,12)),
    ("payment_amount_3","000000000000",12,"\x00",lambda x: rjust_zero(x,12)),
    ("payment_amount_4","000000000000",12,"\x00",lambda x: rjust_zero(x,12)),
    ("payment_amount_5","000000000000",12,"\x00",lambda x: rjust_zero(x,12)),
    ("payment_amount_6","000000000000",12,"\x00",lambda x: rjust_zero(x,12)),
    ("payment_amount_7","000000000000",12,"\x00",lambda x: rjust_zero(x,12)),
    ("payment_amount_8","000000000000",12,"\x00",lambda x: rjust_zero(x,12)),
    ("payment_amount_9","000000000000",12,"\x00",lambda x: rjust_zero(x,12)),
    ("payment_amount_A","000000000000",12,"\x00",lambda x: rjust_zero(x,12)),
    ("payment_amount_B","000000000000",12,"\x00",lambda x: rjust_zero(x,12)),
    ("payment_amount_C","000000000000",12,"\x00",lambda x: rjust_zero(x,12)),
    ("payment_amount_D","000000000000",12,"\x00",lambda x: rjust_zero(x,12)),
    ("payment_amount_E","000000000000",12,"\x00",lambda x: rjust_zero(x,12)),
    ("payment_amount_F","000000000000",12,"\x00",lambda x: rjust_zero(x,12)),
    ("payment_amount_G","000000000000",12,"\x00",lambda x: rjust_zero(x,12)),
    ("foreign_country_indicator","",1,"\x00",lambda x: (x)),
    ("first_payee_name_line","",40,"\x00",lambda x: uppercase(x)),
    ("second_payee_name_line","",40,"\x00",lambda x: uppercase(x)),
    ("blank_2","",40,"\x00",lambda x: (x)),
    ("payee_mailing_address","",40,"\x00",lambda x: (x)),
    ("blank_3","",40,"\x00",lambda x: (x)),
    ("payee_city","",40,"\x00",lambda x: (x)),
    ("payee_state","",2,"\x00",lambda x: (x)),
    ("payee_zip_code","",9,"\x00",lambda x: (x)),
    ("blank_4","",1,"\x00",lambda x: (x)),
    ("record_sequence_number","00000003",8,"\x00",lambda x: rjust_zero(x,8)),
    ("blank_5","",36,"\x00",lambda x: (x)),
    ("second_tin_notice","",1,"\x00",lambda x: (x)),
    ("blank_6","",2,"\x00",lambda x: (x)),
    ("direct_sales_indicator","",1,"\x00",lambda x: (x)),
    ("fatca_filing_requirement_indicator","",1,"\x00",lambda x: (x)),
    ("blank_7","",114,"\x00",lambda x: (x)),
    ("special_data_entries","",60,"\x00",lambda x: (x)),
    ("state_income_tax_withheld","",12,"\x00",lambda x: (x)),
    ("local_income_tax_withheld","",12,"\x00",lambda x: (x)),
    ("combined_federal_state_code","",2,"\x00",lambda x: (x)),
    ("blank_8","",2,"\x00",lambda x: (x))
]

_PAYEE_TRANSFORMS = transform_dict(_PAYEE_TRANSFORMS_ARR)
_PAYEE_SORT = [
    "record_type", "payment_year", "corrected_return_indicator",
    "payees_name_control", "type_of_tin", "payees_tin",
    "payers_account_number_for_payee", "payers_office_code", "blank_1",
    "payment_amount_1", "payment_amount_2", "payment_amount_3",
    "payment_amount_4", "payment_amount_5", "payment_amount_6",
    "payment_amount_7", "payment_amount_8", "payment_amount_9",
    "payment_amount_A", "payment_amount_B", "payment_amount_C",
    "payment_amount_D", "payment_amount_E", "payment_amount_F",
    "payment_amount_G", "foreign_country_indicator", "first_payee_name_line",
    "second_payee_name_line", "blank_2", "payee_mailing_address", "blank_3",
    "payee_city", "payee_state", "payee_zip_code", "blank_4",
    "record_sequence_number", "blank_5", "second_tin_notice", "blank_6",
    "direct_sales_indicator", "fatca_filing_requirement_indicator", "blank_7",
    "special_data_entries", "state_income_tax_withheld",
    "local_income_tax_withheld", "combined_federal_state_code", "blank_8"
]

def xform(data):
    """
    Applies transformation functions definted in _PAYEE_TRANSFORMS to data
    supplied as parameter.

    Parameters
    ----------
    data : array[dict]
        Array of dict elements containing Payee data.
        Expects element of the array to have keys that exist in the 
        _PAYEE_TRANSFORMS dict (not required to have all keys).

    Returns
    ----------
    dict
        Dictionary containing processed (transformed) data provided as a
        parameter.
    """
    payees = []
    for payee in data:
        payees.append(xform_entity(_PAYEE_TRANSFORMS, payee))
    return payees

def fire(data):
    """
    Returns a string formatted to the IRS Publication 1220 specification based
    on data supplied as parameter.

    Parameters
    ----------
    data : array[dict]
        Expects data elements to have all keys specified in _PAYEE_TRANSFORMS.

    Returns
    ----------
    str
        String formatted to meet IRS Publication 1220
    """
    payees_string = ""
    for payee in data:
        payees_string += fire_entity(
            _PAYEE_TRANSFORMS,
            [field[0] for field in _PAYEE_TRANSFORMS_ARR],
            payee)
    return payees_string
