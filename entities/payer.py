"""
Module: entities.payer
Representation of a "payer" record, including transformation functions
and support functions for conversion into different formats.
"""
from translator.util import digits_only, uppercase, rjust_zero
from translator.util import xform_entity, fire_entity, transform_dict

"""
_PAYER_TRANSFORMS
-----------------------
Stores metadata associated with each field in a Transmitter record. 
Values in key-value pairs represent metadata in the following format:

(default value, length, fill character, transformation function)

WARNING
------- 
any edits to the keys or key names must be reflected in the SORT 
array.
"""
_PAYER_TRANSFORMS_ARR = [
    ("record_type","A",1,"\x00",lambda x: x),
    ("payment_year","",4,"\x00",lambda x: digits_only(x)),
    ("combined_fed_state","",1,"\x00",lambda x: x),
    ("blank_1","",5,"\x00",lambda x: x),
    ("payer_tin","",9,"\x00",lambda x: digits_only(x)),
    ("payer_name_control","",4,"\x00",lambda x: uppercase(x)),
    ("last_filing_indicator","",1,"\x00",lambda x: x),
    ("type_of_return","A",2,"\x00",lambda x: uppercase(x)),
    ("amount_codes","7",16,"\x00",lambda x: x),
    ("blank_2","",8,"\x00",lambda x: x),
    ("foreign_entity_indicator","",1,"\x00",lambda x: x),
    ("first_payer_name","",40,"\x00",lambda x: uppercase(x)),
    ("second_payer_name","",40,"\x00",lambda x: uppercase(x)),
    ("transfer_agent_control","0",1,"\x00",lambda x: x),
    ("payer_shipping_address","",40,"\x00",lambda x: uppercase(x)),
    ("payer_city","",40,"\x00",lambda x: uppercase(x)),
    ("payer_state","",2,"\x00",lambda x: uppercase(x)),
    ("payer_zip_code","",9,"\x00",lambda x: digits_only(x)),
    ("payer_telephone_number_and_ext","",15,"\x00",lambda x: digits_only(x)),
    ("blank_3","",260,"\x00",lambda x: x),
    ("record_sequence_number","00000002",8,"\x00",lambda x: rjust_zero(x,8)),
    ("blank_4","",241,"\x00",lambda x: x),
    ("blank_5","",2,"\x00",lambda x: x)
]

_PAYER_TRANSFORMS = transform_dict(_PAYER_TRANSFORMS_ARR)

def xform(data):
    """
    Applies transformation functions definted in _PAYER_TRANSFORMS to data
    supplied as parameter to respective key-value pairs provided as the
    input parameter.

    Parameters
    ----------
    data : dict
        Expects data parameter to have keys that exist in the 
        _PAYER_TRANSFORMS dict.

    Returns
    ----------
    dict
        Dictionary containing processed (transformed) data provided as a
        parameter.
    """
    return xform_entity(_PAYER_TRANSFORMS, data)

def fire(data):
    """
    Returns the given record as a string formatted to the IRS Publication 1220
    specification, based on data supplied as parameter.

    Parameters
    ----------
    data : dict
        Expects data parameter to have all keys specified in _PAYER_TRANSFORMS.

    Returns
    ----------
    str
        String formatted to meet IRS Publication 1220
    """
    return fire_entity(_PAYER_TRANSFORMS,
                       [field[0] for field in _PAYER_TRANSFORMS_ARR],
                       data)
