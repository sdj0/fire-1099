"""
Module: entities.end_of_payer
Representation of an "end_of_payer" record, including transformation functions
and support functions for conversion into different formats.
"""
from translator.util import rjust_zero
from translator.util import xform_entity, fire_entity, transform_dict

"""
_END_OF_PAYER_TRANSFORMS
-----------------------
Stores metadata associated with each field in a Transmitter record. 
Values in key-value pairs represent metadata in the following format:

(default value, length, fill character, transformation function)
"""
_END_OF_PAYER_TRANSFORMS_ARR = [
    ("record_type", "C", 1, "\x00", lambda x: (x)),
    ("number_of_payees", "", 8, "0", lambda x: (x)),
    ("blank_1", "", 6, "\x00", lambda x: (x)),
    ("payment_amount_1", 18*"0", 18, "0", lambda x: rjust_zero(x, 18)),
    ("payment_amount_2", 18*"0", 18, "0", lambda x: rjust_zero(x, 18)),
    ("payment_amount_3", 18*"0", 18, "0", lambda x: rjust_zero(x, 18)),
    ("payment_amount_4", 18*"0", 18, "0", lambda x: rjust_zero(x, 18)),
    ("payment_amount_5", 18*"0", 18, "0", lambda x: rjust_zero(x, 18)),
    ("payment_amount_6", 18*"0", 18, "0", lambda x: rjust_zero(x, 18)),
    ("payment_amount_7", 18*"0", 18, "0", lambda x: rjust_zero(x, 18)),
    ("payment_amount_8", 18*"0", 18, "0", lambda x: rjust_zero(x, 18)),
    ("payment_amount_9", 18*"0", 18, "0", lambda x: rjust_zero(x, 18)),
    ("payment_amount_A", 18*"0", 18, "0", lambda x: rjust_zero(x, 18)),
    ("payment_amount_B", 18*"0", 18, "0", lambda x: rjust_zero(x, 18)),
    ("payment_amount_C", 18*"0", 18, "0", lambda x: rjust_zero(x, 18)),
    ("payment_amount_D", 18*"0", 18, "0", lambda x: rjust_zero(x, 18)),
    ("payment_amount_E", 18*"0", 18, "0", lambda x: rjust_zero(x, 18)),
    ("payment_amount_F", 18*"0", 18, "0", lambda x: rjust_zero(x, 18)),
    ("payment_amount_G", 18*"0", 18, "0", lambda x: rjust_zero(x, 18)),
    ("blank_2", "", 196, "\x00", lambda x: (x)),
    ("record_sequence_number", "", 8, "0", lambda x: (x)),
    ("blank_3", "", 241, "\x00", lambda x: (x)),
    ("blank_4", "", 2, "\x00", lambda x: (x))
]

_END_OF_PAYER_TRANSFORMS = transform_dict(_END_OF_PAYER_TRANSFORMS_ARR)

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
    return fire_entity(_END_OF_PAYER_TRANSFORMS,
                       [field[0] for field in _END_OF_PAYER_TRANSFORMS_ARR],
                       data)
