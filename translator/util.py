"""
Module: Util
Defines a set of classes and functions shared by other modules within 
the fire-1099 application.
"""
import re

# SequenceGenerator: generates sequential integer numbers
class SequenceGenerator:
    """
    Generates sequence nubmers via the get_next() method. Not intended for use 
    in concurrent applications, as increment and string formatting operations 
    (as well as return) are not executed atomically.

    Attributes
    ----------
    self.counter : int
        Maintains the last-used sequence number.

    Methods
    ----------
    str get_next():
        Increments the sequence number represented by self.counter, and returns
        it in the format specified by IRS Publication 1220.
    """
    def __init__(self):
        self.counter = 0
    
    def get_next(self):
        """
        Returns the next sequence number, formatted as a string according to 
        IRS Publication 1220.

        Returns
        ---------
        str
            Sequence number.
        """
        self.counter += 1
        return f"{self.counter:0>8}"

    def get_current(self):
        """
        Returns the current sequence number. Does not format or increment.

        Returns
        ---------
        int
            Sequence number.

        """
        return self.counter

########## Entity support functions ##########

def xform_entity(entity_dict, data):
    """
    Applies transformation functions specified by the entity dictionary (first 
    param) to the user-supplied data (second param). If no user data is
    supplied for the given field in the entity dictionary, then the default
    value for the field is supplied.

    Parameters
    ----------
    entity_dict: dict
        Dictionary containing all fields required for the type of record 
        in question. Expected format of this dict is {"key": (value)} where 
        value is a tuple in the following format:

        (default value, length, fill character, transformation function)

    data: dict
        Data to be transformed and inserted into the returned dict.
        All keys in this dict are expected to be present in entity_dict.

    Returns
    ----------
    dict    
        Dictionary containing all fields specified in parameter "entity_dict",
        with transformed values from parameter "data" or defaults.

    """
    data_dict = {}
    for key, (default, _, _, transform) in entity_dict.items():
        if key in data:
            data_dict[key] = transform(data[key])
        else:
            data_dict[key] = default
    return data_dict

def fire_entity(entity_dict, key_ordering, data, expected_length=750):
    """
    Applies transformation functions specified by the entity dictionary (first
    param) to the user-supplied data (second param). If no user data is
    supplied for the given field in the entity dictionary, then the default
    value for the field is supplied.

    Parameters
    ----------
    entity_dict: dict
        Dictionary containing all fields required for the type of record 
        in question. Expected format of this dict is {"key": (value)} where
        value is a tuple in the following format:

        (default value, length, fill character, transformation function)

    data: dict
        Data to be transformed and inserted into the returned dict. 
        All keys in this dict are expected to be present in entity_dict.

    Returns
    ----------
    dict
        Dictionary containing all fields specified in parameter "entity_dict",
        with transformed values from parameter "data" or defaults.

    """
    record_string = ""
    for key in key_ordering:
        _, length, fill_char, _ = entity_dict[key]
        new_string = data[key].ljust(length, fill_char)
        record_string += new_string
        if len(new_string) != length:
            raise Exception(f"Generated a record string of incorrect length: \
                    Expected: {length} -- Actual: {len(new_string)} \
                    -- Key: {key} -- Value: {record_string}")
    if len(record_string) != expected_length:
        raise Exception(f"Generated records string of invalid length: \
                    {len(record_string)}")
    return record_string

"""
Transformations on user-supplied data
-------------------------------------
Many attributes in each record / entity type share similar
formatting requirements according to IRS Pub 1220. For example, most text 
fields are required to contain uppercase characters. 

The functions below facilitate transformations that are similar across 
different fields and entities.
"""

"""
digits_only(str): Removes all non-digit characters"""
def digits_only(value):
    return re.sub("[^0-9]*", "", value)

"""
uppercase(str): returns the string with all alpha characters in uppercase"""
def uppercase(value):
    return value.upper()

"""
rjust_zer(str, int): right-justifies *value* and pads with zeros to *length*"""
def rjust_zero(value, length):
    return f"{digits_only(value):0>{length}}"

def factor_transforms(transforms):
    """
    Factor a list of transform tuples into a list of sort keys and a dict of
    transforms

    Parameters
    ----------
    transforms : list of tuple
                 The transforms to factor

    Returns
    -------
    sort_keys : list of str
                The names of the transforms, in their original order
    transform_dict : dict of tuple
                     A dict of the transforms, keyed by their sort key
    """
    sort_keys = list()
    transform_dict = dict()

    for transform_name, transform in transforms:
        sort_keys.append(transform_name)
        transform_dict[transform_name] = transform

    return sort_keys, transform_dict
