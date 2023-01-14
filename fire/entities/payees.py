"""
Module: entities.payees
Representation of a "payee" record, including transformation functions
and support functions for conversion into different formats.

Support functions are built to handle arrays of payees (as opposed to
an individual payee)
"""
from itertools import chain

from fire.translator.util import digits_only, uppercase, rjust_zero
from fire.translator.util import factor_transforms, xform_entity, fire_entity
"""
_PAYEE_TRANSFORMS
-----------------------
Stores metadata associated with each field in a Transmitter record.
Values in key-value pairs represent metadata in the following format:

(default value, length, fill character, transformation function)
"""

_ITEMS = [
    ("record_type", ("B", 1, "\x00", lambda x: x)),
    ("payment_year", ("", 4, "\x00", lambda x: x)),
    ("corrected_return_indicator", ("", 1, "\x00", uppercase)),
    ("payees_name_control", ("", 4, "\x00", uppercase)),
    ("type_of_tin", ("1", 1, "\x00", lambda x: x)),
    ("payees_tin", ("000000000", 9, "\x00", digits_only)),
    ("payers_account_number_for_payee", ("", 20, "\x00", lambda x: x)),
    ("payers_office_code", ("", 4, "\x00", lambda x: x)),
    ("blank_1", ("", 10, "\x00", lambda x: x))
]

for field in chain((x for x in range(1, 10)), \
                   (chr(x) for x in range(ord('A'), ord('I'))), \
                   'J'):
    _ITEMS.append((f"payment_amount_{field}",
                   ("000000000000", 12, "\x00", lambda x: rjust_zero(x, 12))))

_ITEMS += [
    ("blank_2", ("", 16, "\x00", lambda x: x)),
    ("foreign_country_indicator", ("", 1, "\x00", lambda x: x)),
    ("first_payee_name_line", ("", 40, "\x00", uppercase)),
    ("second_payee_name_line", ("", 40, "\x00", uppercase)),
    ("payee_mailing_address", ("", 40, "\x00", lambda x: x)),
    ("blank_3", ("", 40, "\x00", lambda x: x)),
    ("payee_city", ("", 40, "\x00", lambda x: x)),
    ("payee_state", ("", 2, "\x00", lambda x: x)),
    ("payee_zip_code", ("", 9, "\x00", lambda x: x)),
    ("blank_4", ("", 1, "\x00", lambda x: x)),
    ("record_sequence_number",
     ("00000003", 8, "\x00", lambda x: rjust_zero(x, 8))),
    ("blank_5", ("", 36, "\x00", lambda x: x)),
    ("second_tin_notice", ("", 1, "\x00", lambda x: x)),
    ("blank_6", ("", 2, "\x00", lambda x: x)),
    ("direct_sales_indicator", ("", 1, "\x00", lambda x: x)),
    ("fatca_filing_requirement_indicator", ("", 1, "\x00", lambda x: x)),
    ("blank_7", ("", 114, "\x00", lambda x: x)),
    ("special_data_entries", ("", 60, "\x00", lambda x: x)),
    ("state_income_tax_withheld", ("", 12, "\x00", lambda x: x)),
    ("local_income_tax_withheld", ("", 12, "\x00", lambda x: x)),
    ("combined_federal_state_code", ("", 2, "\x00", lambda x: x)),
    ("blank_8", ("\x0a\x0a", 2, "\x00", lambda x: x))
]

_PAYEE_SORT, _PAYEE_TRANSFORMS = factor_transforms(_ITEMS)

def xform(data):
    """
    Applies transformation functions definted in _PAYEE_TRANSFORMS to data
    supplied as parameter.

    Parameters
    ----------
    data : array[dict]
        Array of dict elements containing Payee data.
        Expects element of the array to have keys that exist in the
        _PAYEE_TRANSFORMS dict (not required to have all keys).

    Returns
    ----------
    dict
        Dictionary containing processed (transformed) data provided as a
        parameter.
    """
    payees = []
    for payee in data:
        payees.append(xform_entity(_PAYEE_TRANSFORMS, payee))
    return payees

def fire(data):
    """
    Returns a string formatted to the IRS Publication 1220 specification based
    on data supplied as parameter.

    Parameters
    ----------
    data : array[dict]
        Expects data elements to have all keys specified in _PAYEE_TRANSFORMS.

    Returns
    ----------
    str
        String formatted to meet IRS Publication 1220
    """
    payees_string = ""
    for payee in data:
        payees_string += fire_entity(_PAYEE_TRANSFORMS, _PAYEE_SORT, payee)
    return payees_string
