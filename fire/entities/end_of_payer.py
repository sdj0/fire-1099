"""
Module: entities.end_of_payer
Representation of an "end_of_payer" record, including transformation functions
and support functions for conversion into different formats.
"""
from itertools import chain

from fire.translator.util import rjust_zero
from fire.translator.util import factor_transforms, xform_entity, fire_entity

"""
_END_OF_PAYER_TRANSFORMS
-----------------------
Stores metadata associated with each field in a Transmitter record.
Values in key-value pairs represent metadata in the following format:

(default value, length, fill character, transformation function)
"""

_ITEMS = [
    ("record_type", ("C", 1, "\x00", lambda x: x)),
    ("number_of_payees", ("", 8, "0", lambda x: x)),
    ("blank_1", ("", 6, "\x00", lambda x: x)),
]

for field in chain((x for x in range(1, 10)), \
                   (chr(x) for x in range(ord('A'), ord('I'))), \
                   'J'):
    _ITEMS.append((f"payment_amount_{field}",
                   (18*"0", 18, "0", lambda x: rjust_zero(x, 18))))

_ITEMS += [
    ("blank_2", ("", 160, "\x00", lambda x: x)),
    ("record_sequence_number", ("", 8, "0", lambda x: x)),
    ("blank_3", ("", 241, "\x00", lambda x: x)),
    ("blank_4", ("\x0a\x0a", 2, "\x00", lambda x: x))
]

_END_OF_PAYER_SORT, _END_OF_PAYER_TRANSFORMS = factor_transforms(_ITEMS)

def xform(data):
    """
    Applies transformation functions definted in _END_OF_PAYER_TRANSFORMS to
    data supplied as parameter to respective key-value pairs provided as the
    input parameter.

    Parameters
    ----------
    data : dict
        Expects data parameter to have keys that exist in the
        _END_OF_PAYER_TRANSFORMS dict.

    Returns
    ----------
    dict
        Dictionary containing processed (transformed) data provided as a
        parameter.
    """
    return xform_entity(_END_OF_PAYER_TRANSFORMS, data)

def fire(data):
    """
    Returns the given record as a string formatted to the IRS Publication 1220
    specification, based on data supplied as parameter.

    Parameters
    ----------
    data : dict
        Expects data parameter to have all keys specified in
        _END_OF_PAYER_TRANSFORMS.

    Returns
    ----------
    str
        String formatted to meet IRS Publication 1220
    """
    return fire_entity(_END_OF_PAYER_TRANSFORMS, _END_OF_PAYER_SORT, data)
