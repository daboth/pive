# Copyright (c) 2014 - 2016, David Bothe
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

# The visualization types determine which charts can be generated out of
# the given dataset.

from dateutil.parser import parse

VISTYPE_STRING = 0;
VISTYPE_NUMERICAL = 1;
VISTYPE_DATETIME = 2;


def get_datapoint_types(datapoint):
    """Determines the datas visualization-types of a given datapoint.
    Valid visualization-types are 'number', 'string' and 'time'"""
    types = []
    for key in list(datapoint.keys()):

        item = datapoint[key]

        # If the datapoint contains a float or int it will
        # be considered as a numerical datapoint.
        if is_float(item) or is_int(item):
            types.append("number")

        # If the item is a string, it may also be formatted as
        # a datetime item.
        if is_string(item):
            if is_date(item):
                types.append("time")
            else:
                types.append("string")

    return types


def is_string(item):
    """Determines if the item is a string type for Python 3 and
    Python 2.7."""
    is_string = False

    # Python 3 string determination.
    if isinstance(item, str):
        is_string = True

    # Python 2.7 workaround to determine strings.
    # Basestring was deprecated in Python 3.
    else:
        try:
            if isinstance(item, basestring):
                is_string = True
        except TypeError:
            pass

    return is_string


def is_date(item):
    """Checks if the item is a date."""
    try:
        parse(item)
        return True
    except ValueError:
        return False


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


def is_dataset_consistent(input_data):
    """Checks the consistency of the dataset. Each item
	must contain the exact datapoint-type as the other."""
    if input_data:
        current = get_datapoint_types(input_data[0])
        for item in input_data[1:]:
            previous = current
            current = get_datapoint_types(item)
            if previous != current:
                return False
    return True
