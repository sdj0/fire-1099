"""
Module: Translator
Processes user-provided JSON file into an output file in the format
required by IRS Publication 1220.

Support notes:
* 1099-MISC files only.
* Singly payer only. For multiple payers, use multiple input files. 
"""
import os.path
import json
from time import gmtime, strftime
from jsonschema import validate
from pprint import pprint
import click

from translator.util import SequenceGenerator
from entities import transmitter, payer, payees, end_of_payer, end_of_transmission

@click.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.option('--output', type=click.Path())

def cli(input_path, output):
    """
    Wrapper and entry point for command line interface.
    
    Parameters
    ----------
    input_path : str
        system path for file containing the user input JSON data
    output : str
        optional system path for the output to be generated

    """
    run(input_path, output)

def run(input_path, output_path):
    """
    Sequentially calls helper functions to fully process :
    * Load user JSON data from input file
    * Transform user data and merge into a master schema 
    * Generate and insert computed values into master
    * Format ASCII string representing user- and system-generated data
    * Write ASCII string to output file 
    
    Parameters
    ----------
    input_path : str
        system path for file containing the user input JSON data
    output : str
        optional system path for the output to be generated

    """
    module_path = os.path.split(os.path.realpath(__file__))[0]
    schema_path = os.path.join(module_path, '../schema', 'base_schema.json')
    input_dirname = os.path.dirname(os.path.abspath(input_path))
    if output_path is None:
        output_path = "{}/output_{}".format(input_dirname, 
            strftime("%Y-%m-%d %H_%M_%S", gmtime()))

    user_data = extract_user_data(input_path)
    validate_user_data(user_data, schema_path)

    master = load_full_schema(user_data)
    insert_generated_values(master)

    ascii_string = get_fire_format(master)
    write_1099_file(ascii_string, output_path)

def extract_user_data(path):
    """
    Opens file at path specified by input parameter. Reads data as JSON and 
    returns a dict containing that JSON data.
    
    Parameters
    ----------
    path : str
        system path for file containing the user input JSON data

    Returns
    ----------
    dict
        JSON data loaded from file at input path
    """
    user_data = {}
    with open(path, mode='r', encoding='utf-8') as file:
        user_data = json.load(file)
    return user_data

def validate_user_data(data, schema_path):
    """
    Validates data (first param) against the base schema (second param)
    
    Parameters
    ----------
    data : dict
        data to be validated

    schema_path: str
        system path for file containing schema to data validate against

    """
    with open(schema_path, mode='r', encoding='utf-8') as schema:
        schema = json.load(schema)
        validate(data, schema)

def load_full_schema(data):
    """
    Merges data into the master schema for records, including fields that were
    not specified in the data originally loaded (such as system-generated fields  
    and optional fields). 
    
    Parameters
    ----------
    data : dict
        JSON data to be merged into master schema

    Returns
    ----------
    dict
        Master schema with all fields provided in input parameter included

    """
    merged_data = {"transmitter": "", "payer": "", "payees": [],
                   "end_of_payer": "", "end_of_transmission": ""}
    merged_data["transmitter"] = transmitter.xform(data["transmitter"])
    merged_data["payer"] = payer.xform(data["payer"])
    merged_data["payees"] = payees.xform(data["payees"])
    merged_data["end_of_payer"] = end_of_payer.xform({})
    merged_data["end_of_transmission"] = end_of_transmission.xform({})

    return merged_data

def insert_generated_values(data):
    """
    Inserts system-generated values into the appropriate fields. _Note: this
    edits the dict object provided as a parameter in-place._

    Examples of fields inserted: [all]::record_sequence_number, 
    payer::number_of_payees, transmitter::total_number_of_payees, etc.

    Parameters
    ----------
    data : dict
        Dictionary containing "master" set of records. It is expected that
        this includes end_of_payer and end_of_transmission records, with all
        fields captured.

    """
    insert_sequence_numbers(data)
    insert_payer_totals(data)
    insert_transmitter_totals(data)

def insert_sequence_numbers(data):
    """
    Inserts sequence numbers into each record, in the following order: 
    transmitter, payer, payee(s) (each in order supplied by user), 
    end of payer, end of transmission. 

    _Note: this edits the input parameter in-place._
    
    Parameters
    ----------
    data : dict
        Dictionary into which sequence numbers will be inserted.

    """
    seq = SequenceGenerator()

    # Warning: order of below statements is important; do not re-arrange
    data["transmitter"]["record_sequence_number"] = seq.get_next()
    data["payer"]["record_sequence_number"] = seq.get_next()
    for payee in data["payees"]:
        payee["record_sequence_number"] = seq.get_next()
    data["end_of_payer"]["record_sequence_number"] = seq.get_next()
    data["end_of_transmission"]["record_sequence_number"] = seq.get_next()

def insert_payer_totals(data):
    """
    Inserts requried values into the payer and end_of_payer records. This
    includes values for the following fields: payment_amount_*, 
    amount_codes, number_of_payees, total_number_of_payees, number_of_a_records.

    _Note: this edits the input parameter in-place._

    Parameters
    ----------
    data : dict
        Dictionary containing payer, payee, and end_of_payer records, into which 
        computed values will be inserted.

    """
    codes = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", 
             "E", "F", "G"]
    totals = [0 for _ in range(len(codes))]
    payer_code_string = ""

    for payee in data["payees"]:
        for i, code in enumerate(codes):
            try:
                totals[i] += int(payee["payment_amount_" + code])
            except ValueError: 
                pass

    for i, (total, code) in enumerate(zip(totals, codes)):
        if total != 0:
            payer_code_string += code
            data["end_of_payer"]["payment_amount_" + code] = f"{total:0>18}"

    data["payer"]["amount_codes"] = str(payer_code_string)
    payee_count = len(data["payees"])
    data["payer"]["number_of_payees"] = f"{payee_count:0>8}"
    data["end_of_payer"]["number_of_payees"] = f"{payee_count:0>8}"

def insert_transmitter_totals(data):
    """
    Inserts requried values into the transmitter and end_of_transmission 
    records. This includes values for the following fields: 
    total_number_of_payees, number_of_a_records.

    _Note: this edits the input parameter in-place._

    Parameters
    ----------
    data : dict
        Dictionary containing transmitter and end_of_transmission records, 
        into which computed values will be inserted.

    """
    payee_count = len(data["payees"])
    data["transmitter"]["total_number_of_payees"] = f"{payee_count:0>8}"
    data["end_of_transmission"]["total_number_of_payees"] = f"{payee_count:0>8}"
    # Force number of A records to "1" as only one payer is supported
    data["end_of_transmission"]["number_of_a_records"] = "00000001"

def get_fire_format(data):
    """
    Returns the input dictionary converted into the string format required by 
    the IRS FIRE electronic filing system. It is expceted that the input 
    dictionary has the following correctly formatted items:
    * transmitter (dict)
    * payer (dict)
    * payees (array of dict objects)
    * end_of_payer (dict)
    * end_of_transmission
    
    Parameters
    ----------
    data : dict
        Dictionary containing records to be processed into a FIRE-formatted  
        string.

    Returns
    ----------
    str
        FIRE-formatted string containing data provided as the input parameter.
    
    """
    fire_string = ""

    fire_string += transmitter.fire(data["transmitter"])
    fire_string += payer.fire(data["payer"])
    fire_string += payees.fire(data["payees"])
    fire_string += end_of_payer.fire(data["end_of_payer"])
    fire_string += end_of_transmission.fire(data["end_of_transmission"])
    
    return fire_string

def write_1099_file(formatted_string, path):
    """
    Writes the given string to a file at the given path. If the file does not
    exist, it will be created.
    
    Parameters
    ----------
    formatted_string : str
        FIRE-formatted string to be written to disk.

    path: str
        Path of file to be written.

    """
    file = open(path, mode='w+')
    file.write(formatted_string)
    file.close()
