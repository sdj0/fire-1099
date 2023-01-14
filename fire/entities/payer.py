"""
Module: entities.payer
Representation of a "payer" record, including transformation functions
and support functions for conversion into different formats.
"""
from fire.translator.util import digits_only, uppercase, rjust_zero
from fire.translator.util import factor_transforms, xform_entity, fire_entity

"""
_PAYER_TRANSFORMS
-----------------------
Stores metadata associated with each field in a Transmitter record.
Values in key-value pairs represent metadata in the following format:

(default value, length, fill character, transformation function)
"""

_ITEMS = [
    ("record_type", ("A", 1, "\x00", lambda x: x)),
    ("payment_year", ("", 4, "\x00", digits_only)),
    ("combined_fed_state", ("", 1, "\x00", lambda x: x)),
    ("blank_1", ("", 5, "\x00", lambda x: x)),
    ("payer_tin", ("", 9, "\x00", digits_only)),
    ("payer_name_control", ("", 4, "\x00", uppercase)),
    ("last_filing_indicator", ("", 1, "\x00", lambda x: x)),
    ("type_of_return", ("A", 2, "\x00", uppercase)),
    ("amount_codes", ("7", 16, "\x00", lambda x: x)),
    ("blank_2", ("", 8, "\x00", lambda x: x)),
    ("foreign_entity_indicator", ("", 1, "\x00", lambda x: x)),
    ("first_payer_name", ("", 40, "\x00", uppercase)),
    ("second_payer_name", ("", 40, "\x00", uppercase)),
    ("transfer_agent_control", ("0", 1, "\x00", lambda x: x)),
    ("payer_shipping_address", ("", 40, "\x00", uppercase)),
    ("payer_city", ("", 40, "\x00", uppercase)),
    ("payer_state", ("", 2, "\x00", uppercase)),
    ("payer_zip_code", ("", 9, "\x00", digits_only)),
    ("payer_telephone_number_and_ext", ("", 15, "\x00", digits_only)),
    ("blank_3", ("", 260, "\x00", lambda x: x)),
    ("record_sequence_number",
     ("00000002", 8, "\x00", lambda x: rjust_zero(x, 8))),
    ("blank_4", ("", 241, "\x00", lambda x: x)),
    ("blank_5", ("\x0a\x0a", 2, "\x0a", lambda x: x))
]

_PAYER_SORT, _PAYER_TRANSFORMS = factor_transforms(_ITEMS)

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
    return fire_entity(_PAYER_TRANSFORMS, _PAYER_SORT, data)
