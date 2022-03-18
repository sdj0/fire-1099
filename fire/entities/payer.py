"""
Module: entities.payer
Representation of a "payer" record, including transformation functions
and support functions for conversion into different formats.
"""
from fire.translator.util import digits_only, uppercase, rjust_zero
from fire.translator.util import factor_transforms, xform_entity, fire_entity
from fire.translator import global_vars
"""
_PAYER_TRANSFORMS
-----------------------
Stores metadata associated with each field in a Transmitter record.
Values in key-value pairs represent metadata in the following format:

(default value, length, fill character, transformation function)
"""

class Items:

    _PAYER_SORT = {}
    _PAYER_TRANSFORMS = {}


    def __init__(self):

        if not Items._PAYER_SORT or not Items._PAYER_TRANSFORMS:
            Items._PAYER_SORT, Items._PAYER_TRANSFORMS = factor_transforms(Items.get_items())


    def get_items():

        type_of_return = ""

        if global_vars.format_type == "MISC":
            type_of_return = "A"
        elif global_vars.format_type == "NEC":
            type_of_return = "NE"

        return [
            ("record_type", ("A", 1, "\x00", lambda x: x)),
            ("payment_year", ("", 4, "\x00", digits_only)),
            ("combined_fed_state", ("", 1, "\x00", lambda x: x)),
            ("blank_1", ("", 5, "\x00", lambda x: x)),
            ("payer_tin", ("", 9, "\x00", digits_only)),
            ("payer_name_control", ("", 4, "\x00", uppercase)),
            ("last_filing_indicator", ("", 1, "\x00", lambda x: x)),
            ("type_of_return", (type_of_return, 2, "\x00", uppercase)),
            ("amount_codes", ("", 18, "\x00", lambda x: x)),
            ("blank_2", ("", 6, "\x00", lambda x: x)),
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
            ("blank_5", ("", 2, "\x00", lambda x: x))
        ]


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
    _ITEMS = Items()
    return xform_entity(_ITEMS._PAYER_TRANSFORMS, data)

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
    _ITEMS = Items()
    #pprint(_ITEMS.__dict__)
    return fire_entity(_ITEMS._PAYER_TRANSFORMS, _ITEMS._PAYER_SORT, data)
