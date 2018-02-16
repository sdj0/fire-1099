"""
Utility functions used in test specs.
"""
import jsonschema
from jsonschema import validate
import json

from copy import deepcopy
from nose.tools import *

SCHEMA = json.load(open("../schema/base_schema.json"))
VALID_ALL_PATH = "./data/valid_all.json"
INVALID_PHONE_NUMS = ["+1 555 666 7777", "555 A44 B777", "123ABC5678",
                      "123 45 67", "555 666 777788", "555 666 7777 #"]
VALID_PHONE_NUMS = ["5556667777", "555-666-7777", "(555)666-7777", 
                    "(555) 666 7777", "555.666.7777", "(555)-666-7777", 
                    "(555) 666-7777"]
VALID_TINS = ["12-1234567", "121234567", "12 1234567", 
              "111-11-1111", "222 22 2222"]
INVALID_TINS = ["12-12345678", "12-123456", "12-12345-6", "12-ABCDEFG", 
                "111-1-1111", "111-111-111", "1111-11-1111"]

VALID_EMAILS = ["ASDF@asdf.com", "test@test.test.test", "abc1234_234@a.ccc"]
INVALID_EMAILS = ["asdf@asdf@asdf.com", "noat.com", "@noname.com", "nodomain@",
                  "test@rootonly"]

VALID_ZIPS = ["10013", "10013-1001", "11111 2020", "111111111"]
INVALID_ZIPS = ["1001", "11111-11111", "1111111111", "11-11"]

VALID_DOLLAR_AMOUNTS = ["1234500", "12345.00", "1,234,567.00", "$1.00", "$.01",
                        ".01", "0.01", "123,45600"]
INVALID_DOLLAR_AMOUNTS = ["ABCD", "$", "&123,456.00", "€1.00", "0$12.01",
                          "A$12.01" "€100"]

# Map of offsets that should be blank in transmitter ASCII string. Format:
#   (first_byte:last_byte) note that references are 1-indexed
TRANSMITTER_BLANK_MAP = [
    (21, 27),
    (281, 295),
    (409, 499),
    (508, 517),
    (705, 739),
    (741, 750)
]

PAYER_BLANK_MAP = [
    (7, 11),
    (44, 51),
    (240, 499),
    (508, 750)
]

PAYEE_BLANK_MAP = [
    (45, 54),
    (328, 367),
    (408, 447),
    (499, 499),
    (508, 543),
    (723, 750)
]

END_OF_PAYER_BLANK_MAP = [
    (10, 15),
    (304, 499),
    (508, 750)
]

END_OF_TRANSMISSION_BLANK_MAP = [
    (10, 15),
    (304, 499),
    (508, 706),
    (743, 746),
    (749, 750)
]

VALID_ALL_DATA = {}
with open(VALID_ALL_PATH, mode='r', encoding='utf-8') as valid_all_file:
    VALID_ALL_DATA = json.load(valid_all_file)

"""
Locates a key-value pair a multi-tier dict, and overwrites the value
at that with the provided value.

Parameters:
-----------
full_dictionary: dict
    The dictionary containing the value to be modified.

path: list
    List containing the path of the key to be modified, e.g.
    ["top_level_object", "second_level_object", "key_to_be_modified"].

value: object
    The new value to insert at the key given by 'path' parameter.

Returns:
-----------
dict
    New dictionary wherein the key specified by 'path' parameter has the value
    specified by the 'value' parameter. 
"""
def dive_to_path(full_dictionary, path, value):
    def _dive_recursion(sub_dict, path, value):
        if len(path) > 1:
            sub_dict[path[0]] = \
                _dive_recursion(sub_dict[path[0]], path[1:], value)
        if len(path) == 1:
            sub_dict[path[0]] = value
            return sub_dict
        return sub_dict
    dict_copy = deepcopy(full_dictionary)
    return _dive_recursion(dict_copy, path, value)

def check_blanks(sub_string):
    assert sub_string == len(sub_string)*"\x00"

@raises(jsonschema.exceptions.ValidationError)
def check_value_too_long(dict_obj, path, value):
    temp_obj = dive_to_path(dict_obj, path, value)
    validate(temp_obj, SCHEMA)

@raises(jsonschema.exceptions.ValidationError)
def check_invalid_phone_num(dict_obj, path, num):
    temp_obj = dive_to_path(dict_obj, path, num)
    validate(temp_obj, SCHEMA)

def check_valid_phone_num(dict_obj, path, num):
    temp_obj = dive_to_path(dict_obj, path, num)
    assert validate(temp_obj, SCHEMA) is None, \
        print(f"Phone number: {num}, Object: {dict_obj}")

def check_valid_tin(dict_obj, path, tin):
    temp_obj = dive_to_path(dict_obj, path, tin)
    assert validate(dict_obj, SCHEMA) is None, \
        print(f"TIN: {tin}, Object: {dict_obj}")

@raises(jsonschema.exceptions.ValidationError)
def check_invalid_tin(dict_obj, path, tin):
    temp_obj = dive_to_path(dict_obj, path, tin)
    validate(temp_obj, SCHEMA)

def check_valid_email(dict_obj, path, email):
    temp_obj = dive_to_path(dict_obj, path, email)
    assert validate(dict_obj, SCHEMA) is None, \
        print(f"Email: {email}, Object: {dict_obj}")

@raises(jsonschema.exceptions.ValidationError)
def check_invalid_email(dict_obj, path, email):
    temp_obj = dive_to_path(dict_obj, path, email)
    validate(temp_obj, SCHEMA)

def check_valid_zip(dict_obj, path, zip_code):
    temp_obj = dive_to_path(dict_obj, path, zip_code)
    assert validate(dict_obj, SCHEMA) is None, \
        print(f"Zip Code: {zip_code}, Object: {dict_obj}")

@raises(jsonschema.exceptions.ValidationError)
def check_invalid_zip(dict_obj, path, zip_code):
    temp_obj = dive_to_path(dict_obj, path, zip_code)
    validate(temp_obj, SCHEMA)

def check_valid_amount(dict_obj, path, dollar_amount):
    temp_obj = dive_to_path(dict_obj, path, dollar_amount)
    assert validate(dict_obj, SCHEMA) is None, \
        print(f"Dollar Amount: {dollar_amount}, Object: {dict_obj}")

@raises(jsonschema.exceptions.ValidationError)
def check_invalid_amount(dict_obj, path, dollar_amount):
    temp_obj = dive_to_path(dict_obj, path, dollar_amount)
    validate(temp_obj, SCHEMA)

