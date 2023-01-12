"""
Module: entities.state_totals
Representation of an "state totals" record, including transformation functions
and support functions for conversion into different formats.
"""
from itertools import chain

from fire.translator.util import rjust_zero
from fire.translator.util import factor_transforms, xform_entity, fire_entity

"""
_END_OF_STATE_TOTALS_TRANSFORMS
-----------------------
Stores metadata associated with each field in a state_totals record.
Values in key-value pairs represent metadata in the following format:

(default value, length, fill character, transformation function)
"""

_ITEMS = [
    ("record_type", ("K", 1, "\x00", lambda x: x)),
    ("number_of_payees", ("", 8, "0", lambda x: x)),
    ("blank_1", ("", 6, "\x00", lambda x: x)),
]

for field in chain((x for x in range(1, 10)), \
                   (chr(x) for x in range(ord('A'), ord('I'))), \
                   'J'):
    _ITEMS.append((f"control_total_{field}",
                   (18*"0", 18, "0", lambda x: rjust_zero(x, 18))))

_ITEMS += [
    ("blank_2", ("", 160, "\x00", lambda x: x)),
    ("record_sequence_number", ("", 8, "0", lambda x: x)),
    ("blank_3", ("", 199, "\x00", lambda x: x)),
    ("state_income_tax_withheld_total", ("", 18, "\x00", lambda x: x)),
    ("local_income_tax_withheld_total", ("", 18, "\x00", lambda x: x)),
    ("blank_4", ("", 4, "\x00", lambda x: x)),
    ("combined_federal_state_code", ("", 2, "\x00", lambda x: x)),
    ("blank_5", ("\r\n", 2, "\x00", lambda x: x)),
]

_STATE_TOTALS_SORT, _STATE_TOTALS_TRANSFORMS = factor_transforms(_ITEMS)

def xform(data):
    """
    Applies transformation functions definted in _END_OF_STATE_TOTALS_TRANSFORMS to
    data supplied as parameter to respective key-value pairs provided as the
    input parameter.

    Parameters
    ----------
    data : dict
        Expects data parameter to have keys that exist in the
        _END_OF_STATE_TOTALS_TRANSFORMS dict.

    Returns
    ----------
    dict
        Dictionary containing processed (transformed) data provided as a
        parameter.
    """
    return xform_entity(_STATE_TOTALS_TRANSFORMS, data)

def fire(data):
    """
    Returns the given records as a string formatted to the IRS Publication 1220
    specification, based on data supplied as parameter.

    Parameters
    ----------
    data : list of dict
        Expects data parameter to have all keys specified in
        _END_OF_STATE_TOTALS_TRANSFORMS.

    Returns
    ----------
    str
        String formatted to meet IRS Publication 1220
    """
    return ''.join([
        fire_entity(_STATE_TOTALS_TRANSFORMS, _STATE_TOTALS_SORT, state)
        for state in data
    ])
    return fire_entity(_END_OF_STATE_TOTALS_TRANSFORMS, _END_OF_STATE_TOTALS_SORT, data)
