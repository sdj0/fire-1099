
"""
Module: entities.transmitter
Representation of a "transmitter" record, including transformation functions
and support functions for conversion into different formats.
"""
from fire.translator.util import digits_only, uppercase, rjust_zero
from fire.translator.util import factor_transforms, xform_entity, fire_entity

"""
_TRANSMITTER_TRANSFORMS
-----------------------
Stores metadata associated with each field in a Transmitter record.
Values in key-value pairs represent metadata in the following format:

(default value, length, fill character, transformation function)
"""

_ITEMS = [
    ("record_type", ("T", 1, "\x00", lambda x: x)),
    ("payment_year", ("0000", 4, "0", digits_only)),
    ("prior_year_data_indicator", ("", 1, "\x00", uppercase)),
    ("transmitter_tin", ("000000000", 9, "0", digits_only)),
    ("transmitter_control_code", ("", 5, "\x00", uppercase)),
    ("blank_1", ("", 7, "\x00", lambda x: x)),
    ("test_file_indicator", ("T", 1, "\x00", lambda x: x)),
    ("foreign_entity_indicator", ("", 1, "\x00", lambda x: x)),
    ("transmitter_name", ("", 40, "\x00", uppercase)),
    ("transmitter_name_contd", ("", 40, "\x00", uppercase)),
    ("company_name", ("", 40, "\x00", uppercase)),
    ("company_name_contd", ("", 40, "\x00", uppercase)),
    ("company_mailing_address", ("", 40, "\x00", uppercase)),
    ("company_city", ("", 40, "\x00", uppercase)),
    ("company_state", ("", 2, "\x00", uppercase)),
    ("company_zip_code", ("", 9, "\x00", digits_only)),
    ("blank_2", ("", 15, "\x00", lambda x: x)),
    ("total_number_of_payees",
     ("00000000", 8, "0", lambda x: rjust_zero(x, 8))),
    ("contact_name", ("", 40, "\x00", lambda x: x)),
    ("contact_telephone_number_and_ext",
     ("", 15, "\x00", digits_only)),
    ("contact_email_address", ("", 50, "\x00", lambda x: x)),
    ("blank_3", ("", 91, "\x00", lambda x: x)),
    ("record_sequence_number", ("", 8, "\x00", lambda x: x)),
    ("blank_4", ("", 10, "\x00", lambda x: x)),
    ("vendor_indicator", ("I", 1, "\x00", uppercase)),
    ("vendor_name", ("", 40, "\x00", uppercase)),
    ("vendor_mailing_address", ("", 40, "\x00", lambda x: x)),
    ("vendor_city", ("", 40, "\x00", uppercase)),
    ("vendor_state", ("", 2, "\x00", uppercase)),
    ("vendor_zip_code", ("", 9, "\x00", lambda x: x)),
    ("vendor_contact_name", ("", 40, "\x00", uppercase)),
    ("vendor_contact_telephone_and_ext",
     ("", 15, "\x00", digits_only)),
    ("blank_5", ("", 35, "\x00", lambda x: x)),
    ("vendor_foreign_entity_indicator", ("", 1, "\x00", uppercase)),
    ("blank_6", ("", 8, "\x00", lambda x: x)),
    ("blank_7", ("\x0a\x0a", 2, "\x0a", lambda x: x))
]

_TRANSMITTER_SORT, _TRANSMITTER_TRANSFORMS = factor_transforms(_ITEMS)

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
    return fire_entity(_TRANSMITTER_TRANSFORMS, _TRANSMITTER_SORT, data)
