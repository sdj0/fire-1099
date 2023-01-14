"""
Module: entities.extension_of_time
Representation of a "extension_of_time" record, including transformation
functions and support functions for conversion into different formats.
"""
from fire.translator.util import digits_only, uppercase
from fire.translator.util import factor_transforms, xform_entity, fire_entity

"""
EXTENSION_OF_TIME_TRANSFORMS
-----------------------
Stores metadata associated with each field in an Extension of Time record.
Values in key-value pairs represent metadata in the following format:

(default value, length, fill character, transformation function)
"""

_ITEMS = [
    ("transmitter_control_code", ("", 5, "\x00", uppercase)),
    ("payer_tin", ("", 9, "\x00", digits_only)),
    ("first_payer_name", ("", 40, "\x00", uppercase)),
    ("second_payer_name", ("", 40, "\x00", uppercase)),
    ("payer_shipping_address", ("", 40, "\x00", uppercase)),
    ("payer_city", ("", 40, "\x00", uppercase)),
    ("payer_state", ("", 2, "\x00", uppercase)),
    ("payer_zip_code", ("", 9, "\x00", digits_only)),
    ("document_indicator", ("A", 1, "\x00", lambda x: x)),
    ("foreign_entity_indicator", ("", 1, "\x00", lambda x: x)),
    ("blank_1", ("", 11, "\x00", lambda x: x)),
    ("blank_2", ("\x0a\x0a", 2, "\x00", lambda x: x))
]

_EXTENSION_OF_TIME_SORT, _EXTENSION_OF_TIME_TRANSFORMS = \
    factor_transforms(_ITEMS)

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
    return xform_entity(_EXTENSION_OF_TIME_TRANSFORMS, data)

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
    return fire_entity(_EXTENSION_OF_TIME_TRANSFORMS,
                       _EXTENSION_OF_TIME_SORT, data, 200)
