
"""
Module: entities.transmitter
Representation of a "transmitter" record, including transformation functions
and support functions for conversion into different formats.
"""
from translator.util import digits_only, uppercase, rjust_zero
from translator.util import xform_entity, fire_entity, transform_dict

"""
_TRANSMITTER_TRANSFORMS
-----------------------
Stores metadata associated with each field in a Transmitter record. 
Values in key-value pairs represent metadata in the following format:

(default value, length, fill character, transformation function)

WARNING
------- 
any edits to the keys or key names must be reflected in the SORT 
array. 
"""
_TRANSMITTER_TRANSFORMS_ARR = [
    ("record_type","T",1,"\x00",lambda x: x),
    ("payment_year","0000",4,"0",lambda x: digits_only(x)),
    ("prior_year_data_indicator","",1,"\x00",lambda x: uppercase(x)),
    ("transmitter_tin","000000000",9,"0",lambda x: digits_only(x)),
    ("transmitter_control_code","",5,"\x00",lambda x: uppercase(x)),
    ("blank_1","",7,"\x00",lambda x: x),
    ("test_file_indicator","T",1,"\x00",lambda x: x),
    ("foreign_entity_indicator","",1,"\x00",lambda x: x),
    ("transmitter_name","",40,"\x00",lambda x: uppercase(x)),
    ("transmitter_name_contd","",40,"\x00",lambda x: uppercase(x)),
    ("company_name","",40,"\x00",lambda x: uppercase(x)),
    ("company_name_contd","",40,"\x00",lambda x: uppercase(x)),
    ("company_mailing_address","",40,"\x00",lambda x: uppercase(x)),
    ("company_city","",40,"\x00",lambda x: uppercase(x)),
    ("company_state","",2,"\x00",lambda x: uppercase(x)),
    ("company_zip_code","",9,"\x00",lambda x: digits_only(x)),
    ("blank_2","",15,"\x00",lambda x: x),
    ("total_number_of_payees","00000000",8,"0",lambda x: rjust_zero(x,8)),
    ("contact_name","",40,"\x00",lambda x: x),
    ("contact_telephone_number_and_ext","",15,"\x00",lambda x: digits_only(x)),
    ("contact_email_address","",50,"\x00",lambda x: (x)),
    ("blank_3","",91,"\x00",lambda x: x),
    ("record_sequence_number","",8,"\x00",lambda x: x),
    ("blank_4","",10,"\x00",lambda x: x),
    ("vendor_indicator","I",1,"\x00",lambda x: uppercase(x)),
    ("vendor_name","",40,"\x00",lambda x: uppercase(x)),
    ("vendor_mailing_address","",40,"\x00",lambda x: x),
    ("vendor_city","",40,"\x00",lambda x: uppercase(x)),
    ("vendor_state","",2,"\x00",lambda x: uppercase(x)),
    ("vendor_zip_code","",9,"\x00",lambda x: x),
    ("vendor_contact_name","",40,"\x00",lambda x: uppercase(x)),
    ("vendor_contact_telephone_and_ext","",15,"\x00",lambda x: digits_only(x)),
    ("blank_5","",35,"\x00",lambda x: x),
    ("vendor_foreign_entity_indicator","",1,"\x00",lambda x: uppercase(x)),
    ("blank_6","",8,"\x00",lambda x: x),
    ("blank_7","",2,"\x00",lambda x: x)
]

_TRANSMITTER_TRANSFORMS = transform_dict(_TRANSMITTER_TRANSFORMS_ARR)

def xform(data):
    """
    Applies transformation functions definted in _TRANSMITTER_TRANSFORMS to data
    supplied as parameter to respective key-value pairs provided as the
    input parameter.

    Parameters
    ----------
    data : dict
        Expects data parameter to have keys that exist in the 
        _TRANSMITTER_TRANSFORMS dict.

    Returns
    ----------
    dict
        Dictionary containing processed (transformed) data provided as a
        parameter.
    """
    return xform_entity(_TRANSMITTER_TRANSFORMS, data)

def fire(data):
    """
    Returns the given record as a string formatted to the IRS Publication 1220
    specification, based on data supplied as parameter.

    Parameters
    ----------
    data : dict
        Expects data parameter to have all keys specified in
        _TRANSMITTER_TRANSFORMS.

    Returns
    ----------
    str
        String formatted to meet IRS Publication 1220
    """
    return fire_entity(_TRANSMITTER_TRANSFORMS,
                       [field[0] for field in _TRANSMITTER_TRANSFORMS_ARR],
                       data)
