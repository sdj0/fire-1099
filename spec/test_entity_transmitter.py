# pylint: disable=missing-docstring, invalid-name

from copy import deepcopy

import jsonschema

from jsonschema import validate
from nose.tools import raises

from spec_util import check_blanks, check_value_too_long, \
                      check_valid_phone_num, \
                      check_invalid_phone_num, check_valid_tin, \
                      check_invalid_tin, check_valid_zip, check_invalid_zip, \
                      check_valid_email, check_invalid_email, \
                      SCHEMA, TRANSMITTER_BLANK_MAP, VALID_ALL_DATA, \
                      VALID_PHONE_NUMS, VALID_ZIPS, INVALID_ZIPS, \
                      VALID_EMAILS, INVALID_EMAILS, INVALID_PHONE_NUMS, \
                      VALID_TINS, INVALID_TINS
from fire.entities import transmitter

VALID_TRANSMITTER = {}
VALID_TRANSMITTER["transmitter"] = VALID_ALL_DATA["transmitter"]

"""
Schema validation tests: transmitter
"""
def test_transmitter_schema_ignore_extra_data():
    temp = deepcopy(VALID_TRANSMITTER)
    temp["extraneous_key"] = "should_be_ignored"
    assert validate(temp, SCHEMA) is None, f"Object: {temp}"

def test_transmitter_schema_overly_long_values():
    temp = deepcopy(VALID_TRANSMITTER)
    for key, value in temp["transmitter"].items():
        if isinstance(value, str):
            yield check_value_too_long, \
                temp, ["transmitter", key], value + 99*"A"

def test_transmitter_schema_phone_numbers():
    temp = deepcopy(VALID_TRANSMITTER)
    for num in VALID_PHONE_NUMS:
        yield check_valid_phone_num, \
            temp, ["transmitter", "contact_telephone_number_and_ext"], num
        yield check_valid_phone_num, \
            temp, ["transmitter", "vendor_contact_telephone_and_ext"], num

    for num in INVALID_PHONE_NUMS:
        yield check_invalid_phone_num, \
            temp, ["transmitter", "contact_telephone_number_and_ext"], num
        yield check_invalid_phone_num, \
            temp, ["transmitter", "vendor_contact_telephone_and_ext"], num

def test_transmitter_schema_validation_tins():
    temp = deepcopy(VALID_TRANSMITTER)
    for tin in VALID_TINS:
        yield check_valid_tin, \
            temp, ["transmitter", "transmitter_tin"], tin
    for tin in INVALID_TINS:
        yield check_invalid_tin, \
            temp, ["transmitter", "transmitter_tin"], tin

def test_transmitter_schema_emails():
    temp = deepcopy(VALID_TRANSMITTER)
    for email in VALID_EMAILS:
        yield check_valid_email, \
            temp, ["transmitter", "contact_email_address"], email
    for email in INVALID_EMAILS:
        yield check_invalid_email, \
            temp, ["transmitter", "contact_email_address"], email

def test_transmitter_schema_zip_codes():
    temp = deepcopy(VALID_TRANSMITTER)
    for zip_code in VALID_ZIPS:
        yield check_valid_zip, \
            temp, ["transmitter", "company_zip_code"], zip_code
        yield check_valid_zip, \
            temp, ["transmitter", "vendor_zip_code"], zip_code
    for zip_code in INVALID_ZIPS:
        yield check_invalid_zip, \
            temp, ["transmitter", "company_zip_code"], zip_code
        yield check_invalid_zip, \
            temp, ["transmitter", "vendor_zip_code"], zip_code

@raises(jsonschema.exceptions.ValidationError)
def test_missing_required_data():
    temp = deepcopy(VALID_TRANSMITTER)
    del temp["transmitter"]["transmitter_tin"]
    validate(temp, SCHEMA)

"""
User data transformation tests: transmitter.xform()
"""
def test_transmitter_xform_uppercase():
    temp = deepcopy(VALID_TRANSMITTER)
    temp["transmitter"]["transmitter_name"] = "nocaps mclowercase"
    transformed = transmitter.xform(temp["transmitter"])
    assert transformed["transmitter_name"] == "NOCAPS MCLOWERCASE"

def test_transmitter_xform_remove_punctuation():
    temp = deepcopy(VALID_TRANSMITTER)
    temp["transmitter"]["contact_telephone_number_and_ext"] = "(555)555-5555"
    transformed = transmitter.xform(temp["transmitter"])
    assert transformed["contact_telephone_number_and_ext"] == "5555555555"

def test_transmitter_xform_adds_system_fields():
    temp = deepcopy(VALID_TRANSMITTER)
    assert "blank_2" not in temp
    transformed = transmitter.xform(temp)
    assert "blank_2" in transformed

"""
FIRE-formatted ASCII string generation tests: transmitter.fire()
"""
def test_transmitter_fire_string_length():
    temp = deepcopy(VALID_TRANSMITTER)
    transformed = transmitter.xform(temp["transmitter"])
    test_string = transmitter.fire(transformed)
    assert len(test_string) == 750

def test_transmitter_fire_padding_blanks():
    temp = deepcopy(VALID_TRANSMITTER)
    temp["transmitter"]["company_mailing_address"] = "1234 ROADSTREET AVE"
    transformed = transmitter.xform(temp["transmitter"])
    test_string = transmitter.fire(transformed)
    addr = test_string[189:229]
    assert addr[0:19] == "1234 ROADSTREET AVE"
    assert addr[19:] == 21*"\x00"

def test_transmitter_fire_padding_zeros():
    temp = deepcopy(VALID_TRANSMITTER)
    temp["transmitter"]["total_number_of_payees"] = "2"
    transformed = transmitter.xform(temp["transmitter"])
    test_string = transmitter.fire(transformed)
    num_of_payees = test_string[295:303]
    assert num_of_payees == "00000002"

def test_transmitter_fire_blanks_layout():
    temp = deepcopy(VALID_TRANSMITTER)
    transformed = transmitter.xform(temp["transmitter"])
    test_string = transmitter.fire(transformed)
    for (offset_1_indexed, inclusive_bound) in TRANSMITTER_BLANK_MAP:
        yield check_blanks, test_string[(offset_1_indexed -1):inclusive_bound]
