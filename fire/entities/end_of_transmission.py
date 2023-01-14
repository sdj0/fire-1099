"""
Module: entities.end_of_transmission
Representation of an "end_of_transmission" record, including transformation
functions and support functions for conversion into different formats.
"""
from fire.translator.util import rjust_zero
from fire.translator.util import factor_transforms, xform_entity, fire_entity

"""
_END_OF_TRANSMISSION_TRANSFORMS
-----------------------
Stores metadata associated with each field in a Transmitter record.
Values in key-value pairs represent metadata in the following format:

(default value, length, fill character, transformation function)
"""

_ITEMS = [
    ("record_type", ("F", 1, "\x00", lambda x: x)),
    ("number_of_a_records", ("00000000", 8, "0", lambda x: rjust_zero(x, 8))),
    ("zeros", (21*"0", 21, "0", lambda x: x)),
    ("blank_1", ("", 19, "\x00", lambda x: x)),
    ("total_number_of_payees",
     ("00000000", 8, "0", lambda x: rjust_zero(x, 8))),
    ("blank_2", ("", 442, "\x00", lambda x: x)),
    ("record_sequence_number", ("", 8, "0", lambda x: x)),
    ("blank_3", ("", 241, "\x00", lambda x: x)),
    ("blank_4", ("\x0a\x0a", 2, "\x00", lambda x: x))
]

_END_OF_TRANSMISSION_SORT, _END_OF_TRANSMISSION_TRANSFORMS = \
    factor_transforms(_ITEMS)

def xform(data):
    """
    Applies transformation functions definted in _END_OF_TRANSMISSION_TRANSFORMS
    to data supplied as parameter to respective key-value pairs provided as the
    input parameter.

    Parameters
    ----------
    data : dict
        Expects data parameter to have keys that exist in the
        _END_OF_TRANSMISSION_TRANSFORMS dict.

    Returns
    ----------
    dict
        Dictionary containing processed (transformed) data provided as a
        parameter.
    """
    return xform_entity(_END_OF_TRANSMISSION_TRANSFORMS, data)

def fire(data):
    """
    Returns the given record as a string formatted to the IRS Publication 1220
    specification, based on data supplied as parameter.

    Parameters
    ----------
    data : dict
        Expects data parameter to have all keys specified in
        _END_OF_TRANSMISSION_TRANSFORMS.

    Returns
    ----------
    str
        String formatted to meet IRS Publication 1220
    """
    return fire_entity(
        _END_OF_TRANSMISSION_TRANSFORMS,
        _END_OF_TRANSMISSION_SORT, data)
