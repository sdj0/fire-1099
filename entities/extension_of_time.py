"""
Module: entities.extension_of_time
Representation of a "extension_of_time" record, including transformation
functions and support functions for conversion into different formats.
"""
from translator.util import digits_only, uppercase
from translator.util import xform_entity, fire_entity, transform_dict

"""
EXTENSION_OF_TIME_TRANSFORMS
-----------------------
Stores metadata associated with each field in an Extension of Time record. 
Values in key-value pairs represent metadata in the following format:

(default value, length, fill character, transformation function)
"""
EXTENSION_OF_TIME_TRANSFORMS = {
    "transmitter_control_code":
        ("", 5, "\x00", lambda x: uppercase(x)),
    "payer_tin":
        ("", 9, "\x00", lambda x: digits_only(x)),
    "first_payer_name":
        ("", 40, "\x00", lambda x: uppercase(x)),
    "second_payer_name":
        ("", 40, "\x00", lambda x: uppercase(x)),
    "payer_shipping_address":
        ("", 40, "\x00", lambda x: uppercase(x)),
    "payer_city":
        ("", 40, "\x00", lambda x: uppercase(x)),
    "payer_state":
        ("", 2, "\x00", lambda x: uppercase(x)),
    "payer_zip_code":
        ("", 9, "\x00", lambda x: digits_only(x)),
    "document_indicator":
        ("A", 1, "\x00", lambda x: x),
    "foreign_entity_indicator":
        ("", 1, "\x00", lambda x: x),
    "blank_1":
        ("", 11, "\x00", lambda x: x),
    "blank_2":
        ("", 2, "\x00", lambda x: x)
}

_EXTENSION_OF_TIME_SORT = [
    "transmitter_control_code", "payer_tin", "first_payer_name",
    "second_payer_name", "payer_shipping_address", "payer_city", "payer_state",
    "payer_zip_code", "document_indicator", "foreign_entity_indicator",
    "blank_1", "blank_2"
]

def xform(data):
    """
    Applies transformation functions definted in EXTENSION_OF_TIME_TRANSFORMS
    to data supplied as parameter to respective key-value pairs provided as the
    input parameter.

    Parameters
    ----------
    data : dict
        Expects data parameter to have keys that exist in the 
        EXTENSION_OF_TIME_TRANSFORMS dict.

    Returns
    ----------
    dict
        Dictionary containing processed (transformed) data provided as a
        parameter.
    """
    return xform_entity(EXTENSION_OF_TIME_TRANSFORMS, data)

def fire(data):
    """
    Returns the given record as a string formatted to the IRS Publication 1220
    specification, based on data supplied as parameter.

    Parameters
    ----------
    data : dict
        Expects data parameter to have all keys specified in
        EXTENSION_OF_TIME_TRANSFORMS.

    Returns
    ----------
    str
        String formatted to meet IRS Publication 1220
    """
    return fire_entity(EXTENSION_OF_TIME_TRANSFORMS, 
                       _EXTENSION_OF_TIME_SORT, data, 200)
