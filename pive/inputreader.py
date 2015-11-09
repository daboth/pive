# Copyright (c) 2014 - 2015, David Bothe
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import json
import csv
from collections import OrderedDict


def load_input_source(input_source):
    """Load data from an arbitrary input source. Currently supported:
	JSON, JSON-String, CSV, CSV-String. Returns an empty list if no data
	is available."""
    input_data = []
    try:
        input_data = load_json_from_file(input_source)
    except ValueError as e:
        pass
    except IOError as e:
        pass
    except Exception as e:
        pass
    else:
        return input_data

    if not input_data:
        try:
            input_data = load_json_string(input_source)
        except AttributeError as e:
            pass
        except ValueError as e:
            pass
        except Exception as e:
            pass

    if not input_data:
        try:
            input_data = load_csv_from_file(input_source)
        except csv.Error as e:
            pass
        except IOError as e:
            pass
        except Exception as e:
            pass

    if not input_data:
        try:
            input_data = load_csv_string(input_source)
        except Exception as e:
            pass
    return input_data


def load_json_from_file(json_input):
    """Load a JSON File."""
    fp = open(json_input, 'r')
    inpt = json.load(fp, object_pairs_hook=OrderedDict)
    return inpt


def load_json_string(json_input):
    """Load a JSON-String."""
    inpt = json.loads(json_input, object_pairs_hook=OrderedDict)
    return inpt


def load_csv_string(csv_input):
    """Load a CSV-String."""
    inputstring = csv_input.split('\n')
    data = []
    dialect = csv.Sniffer().sniff(csv_input)
    delimiterchar = dialect.delimiter
    inputdata = csv.DictReader(inputstring)
    header = inputdata.fieldnames

    for row in inputdata:
        od = OrderedDict()

        for item in header:
            value = parse_value_type(row[item])
            od[item] = value
        data.append(od)

    return data


def load_csv_from_file(csv_input):
    """Loads the input from a csv file and returns
	a list of ordered dictionaries for further processing."""
    data = []
    csvfile = open(csv_input)
    csvfile.seek(0)
    dialect = csv.Sniffer().sniff(csvfile.read())
    csvfile.seek(0)
    isHeader = csv.Sniffer().has_header(csvfile.read())
    csvfile.seek(0)
    # The delimiter used in the dialect.
    delimiterchar = dialect.delimiter
    # Opens the input file with the determined delimiter.
    dictreader = csv.DictReader(csvfile, dialect=dialect)

    header = dictreader.fieldnames

    #Translate the data into a list of dictionaries.
    for row in dictreader:

        ordered_data = OrderedDict()
        for item in header:
            value = parse_value_type(row[item])

            ordered_data[item] = value

        data.append(ordered_data)
    return data


def parse_value_type(value):
    if is_int(value):
        value = int(value)
    elif is_float(value):
        value = float(value)
    return value


def is_float(value):
    try:
        number = float(value)
    except ValueError:
        return False
    else:
        return True


def is_int(value):
    try:
        num_a = float(value)
        num_b = int(num_a)
    except ValueError:
        return False
    else:
        return num_a == num_b