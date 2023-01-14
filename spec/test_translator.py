# pylint: disable=missing-docstring, invalid-name

import os
import re

from time import gmtime, strftime

from nose.tools import raises

from spec_util import check_blanks, \
                      PAYER_BLANK_MAP, PAYEE_BLANK_MAP, \
                      END_OF_PAYER_BLANK_MAP, END_OF_TRANSMISSION_BLANK_MAP, \
                      TRANSMITTER_BLANK_MAP, VALID_ALL_DATA, \
                      VALID_ALL_PATH
from fire.translator import translator

# Tests whether a correct input file generates a correct output file
# Tests whether an output file is defaulted if no path is given
OUTPUT_FILE_PREFIX = "./spec/data/test_outfile"

def test_translator_run_full_with_specified_output_file():
    output_path = f"{OUTPUT_FILE_PREFIX}_run_valid.ascii"
    if os.path.isfile(output_path):
        os.remove(output_path)
    translator.run(VALID_ALL_PATH, output_path)
    assert os.path.isfile(output_path)
    with open(output_path, mode='r', encoding='utf-8') as output_file:
        ascii_str = output_file.read()
        assert len(ascii_str) == 4500
    os.remove(output_path)

def test_translator_run_full_with_default_output_file():
    start_len = len([f for f in os.listdir('./spec/data/') if f.startswith(
        "output_{}".format(strftime("%Y-%m-%d", gmtime())))])
    translator.run(VALID_ALL_PATH, None)
    file_names = [f for f in os.listdir('./spec/data/') if f.startswith(
        "output_{}".format(strftime("%Y-%m-%d", gmtime())))]
    assert len(file_names) == start_len + 1
    for file in file_names:
        if file.startswith("output_"):
            os.remove(f"./spec/data/{file}")

@raises(FileNotFoundError)
def test_translator_run_full_process_invalid_path():
    nonexistant_path = "./spec/data/does/not/exist.json"
    if os.path.isfile(nonexistant_path):
        os.remove(nonexistant_path)
    translator.run(VALID_ALL_PATH, nonexistant_path)

########################################################

# Tests the load_full_schema method for correct schema structure, presence
# of records, and inserted user data.
# Should fail if no payer/payee data or no transmitter data (key error), or if
# at value from the user data is not present in the returned dict
def test_translator_load_data_into_schema():
    # pylint: disable=invalid-sequence-index
    merged_data = translator.load_full_schema(VALID_ALL_DATA)
    assert merged_data["transmitter"]["contact_telephone_number_and_ext"] == \
        "5555555555"
    assert merged_data["payer"]["payer_tin"] == "123456789"
    assert len(merged_data["payees"]) == 2
    assert merged_data["end_of_payer"] is not None
    assert merged_data["end_of_transmission"] is not None

# Tests whether sequence numbers start at 1, are sequential (given the specific
# structure of the VALID_ALL_DATA input, and are formatted correctly as
# 8-character strings
def test_translator_insert_sequence_numbers():
    # pylint: disable=invalid-sequence-index
    merged_data = translator.load_full_schema(VALID_ALL_DATA)
    translator.insert_sequence_numbers(merged_data)

    assert merged_data["transmitter"]["record_sequence_number"] == "00000001"
    assert merged_data["payer"]["record_sequence_number"] == "00000002"
    assert merged_data["payees"][0]["record_sequence_number"] == "00000003"
    assert merged_data["payees"][1]["record_sequence_number"] == "00000004"
    assert merged_data["end_of_payer"]["record_sequence_number"] == "00000005"
    assert merged_data["end_of_transmission"]["record_sequence_number"] == \
        "00000006"


# Tests whether payer and end_of_payer record fields are correctly inserted
def test_translator_insert_payer_totals():
    # pylint: disable=invalid-sequence-index
    data = translator.load_full_schema(VALID_ALL_DATA)
    translator.insert_payer_totals(data)

    # Test payer record
    assert data["payer"]["amount_codes"] == "123456789ABCDEFG"
    assert data["payer"]["number_of_payees"] == "00000002"

    # Test end_of_payer record
    # pylint: disable=no-member
    values = [v for (k, v) in data["end_of_payer"].items() if \
              re.match(r"^payment_amount_.", k) and int(v) > 0]
    assert len(values) == 16
    for v in values:
        assert v == "000000000000001700"


# Tests whether a transmitter record has the correct total number of payeers/ees
# entered into the "number_of_a_records" and "total_number_of_payees" fields
def test_translator_insert_transmitter_totals():
    # pylint: disable=invalid-sequence-index
    data = translator.load_full_schema(VALID_ALL_DATA)
    translator.insert_transmitter_totals(data)

    assert data["transmitter"]["total_number_of_payees"] == "00000002"
    assert data["end_of_transmission"]["total_number_of_payees"] == "00000002"
    assert data["end_of_transmission"]["number_of_a_records"] == "00000001"



# Checks whether a FIRE formatted string has the correct length, blank pos,
# and possible user data in the correct places. Checks that record sequnce
# numbers are in the correct order (using offsets)
def test_translator_get_fire_format():
    data = translator.load_full_schema(VALID_ALL_DATA)
    translator.insert_generated_values(data)
    ascii_string = translator.get_fire_format(data)

    assert len(ascii_string) == 4500
    for (offset, inclusive_bound) in TRANSMITTER_BLANK_MAP:
        yield check_blanks, ascii_string[(offset -1):inclusive_bound]

    for (offset, inclusive_bound) in PAYER_BLANK_MAP:
        yield check_blanks, ascii_string[(offset + 749):inclusive_bound]

    for (offset, inclusive_bound) in PAYEE_BLANK_MAP:
        yield check_blanks, ascii_string[(offset + 749*2):inclusive_bound]
        yield check_blanks, ascii_string[(offset + 749*3):inclusive_bound]

    for (offset, inclusive_bound) in END_OF_PAYER_BLANK_MAP:
        yield check_blanks, ascii_string[(offset + 749*4):inclusive_bound]

    for (offset, inclusive_bound) in END_OF_TRANSMISSION_BLANK_MAP:
        yield check_blanks, ascii_string[(offset + 749*5):inclusive_bound]

def test_translator_insert_state_totals():
    """A schema with a state / federal consolidated field should generate a state_totals record."""
    data = translator.load_full_schema(VALID_ALL_DATA)
    data["payees"][0]["combined_federal_state_code"] = "06"
    translator.insert_state_total_records(data)

    assert len(data["state_totals"]) == 1

def test_insert_payer_totals():
    data = translator.load_full_schema(VALID_ALL_DATA)
    data["payees"][0]["combined_federal_state_code"] = "06"
    data["payees"][1]["combined_federal_state_code"] = "06"
    translator.insert_generated_values(data)
    assert int(data["state_totals"][0]["control_total_1"]) == 1700

