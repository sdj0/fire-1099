# pylint: disable=missing-docstring, invalid-name

from copy import deepcopy

import jsonschema

from jsonschema import validate
from nose.tools import raises

from spec_util import check_blanks, check_value_too_long, check_valid_phone_num, \
                      check_invalid_phone_num, check_valid_tin, \
                      check_invalid_tin, check_valid_zip, check_invalid_zip, \
                      SCHEMA, PAYER_BLANK_MAP, VALID_ALL_DATA, \
                      VALID_PHONE_NUMS, VALID_ZIPS, INVALID_ZIPS, \
                      INVALID_PHONE_NUMS, VALID_TINS, INVALID_TINS
from fire.entities import payer

VALID_PAYER = {}
VALID_PAYER["payer"] = VALID_ALL_DATA["payer"]

"""
Schema validation tests: payer
"""
def test_payer_schema_ignore_extra_data():
    temp = deepcopy(VALID_PAYER)
    temp["extraneous_key"] = "should_be_ignored"
    assert validate(temp, SCHEMA) is None, f"Object: {temp}"

def test_payer_schema_overly_long_values():
    temp = deepcopy(VALID_PAYER)
    for key, value in temp["payer"].items():
        if isinstance(value, str):
            yield check_value_too_long, \
                temp, ["payer", key], value + 99*"A"

def test_payer_schema_phone_numbers():
    temp = deepcopy(VALID_PAYER)
    for num in VALID_PHONE_NUMS:
        yield check_valid_phone_num, \
            temp, ["payer", "payer_telephone_number_and_ext"], num

    for num in INVALID_PHONE_NUMS:
        yield check_invalid_phone_num, \
            temp, ["payer", "payer_telephone_number_and_ext"], num

def test_payer_schema_validation_tins():
    temp = deepcopy(VALID_PAYER)
    for tin in VALID_TINS:
        yield check_valid_tin, \
            temp, ["payer", "payer_tin"], tin
    for tin in INVALID_TINS:
        yield check_invalid_tin, \
            temp, ["payer", "payer_tin"], tin

def test_payer_schema_zip_codes():
    temp = deepcopy(VALID_PAYER)
    for zip_code in VALID_ZIPS:
        yield check_valid_zip, \
            temp, ["payer", "payer_zip_code"], zip_code
    for zip_code in INVALID_ZIPS:
        yield check_invalid_zip, \
            temp, ["payer", "payer_zip_code"], zip_code

@raises(jsonschema.exceptions.ValidationError)
def test_missing_required_data():
    temp = deepcopy(VALID_PAYER)
    del temp["payer"]["payer_tin"]
    validate(temp, SCHEMA)

"""
User data transformation tests: payer.xform()
"""
def test_payer_xform_uppercase():
    temp = deepcopy(VALID_PAYER)
    temp["payer"]["first_payer_name"] = "nocaps mclowercase"
    transformed = payer.xform(temp["payer"])
    assert transformed["first_payer_name"] == "NOCAPS MCLOWERCASE"

def test_payer_xform_remove_punctuation():
    temp = deepcopy(VALID_PAYER)
    temp["payer"]["payer_telephone_number_and_ext"] = "(555)555-5555"
    transformed = payer.xform(temp["payer"])
    assert transformed["payer_telephone_number_and_ext"] == "5555555555"

def test_payer_xform_adds_system_fields():
    temp = deepcopy(VALID_PAYER)
    assert "blank_2" not in temp
    transformed = payer.xform(temp)
    assert "blank_2" in transformed

"""
FIRE-formatted ASCII string generation tests: payer.fire()
"""
def test_payer_fire_string_length():
    temp = deepcopy(VALID_PAYER)
    transformed = payer.xform(temp["payer"])
    test_string = payer.fire(transformed)
    assert len(test_string) == 750

def test_payer_fire_padding_blanks():
    temp = deepcopy(VALID_PAYER)
    temp["payer"]["payer_shipping_address"] = "1234 ROADSTREET AVE"
    transformed = payer.xform(temp["payer"])
    test_string = payer.fire(transformed)
    addr = test_string[133:173]

    assert addr[0:19] == "1234 ROADSTREET AVE"
    assert addr[19:] == 21*"\x00"

def test_payer_fire_padding_zeros():
    temp = deepcopy(VALID_PAYER)
    temp["payer"]["record_sequence_number"] = "2"
    transformed = payer.xform(temp["payer"])
    test_string = payer.fire(transformed)
    sequence_num = test_string[499:507]
    assert sequence_num == "00000002"

def test_payer_fire_blanks_layout():
    temp = deepcopy(VALID_PAYER)
    transformed = payer.xform(temp["payer"])
    test_string = payer.fire(transformed)
    for (offset_1_indexed, inclusive_bound) in PAYER_BLANK_MAP:
        yield check_blanks, test_string[(offset_1_indexed -1):inclusive_bound]

#def check_blanks(sub_string):
#    assert sub_string == len(sub_string)*"\x00"
