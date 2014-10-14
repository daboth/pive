# Copyright (c) 2014, David Bothe
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

def getDatapointTypes(datapoint):
    """Determines the datas visualization-types of a given datapoint.
	Valid visualization-types are 'number', 'string' and 'time'"""
    types = []
    for key in list(datapoint.keys()):

        item = datapoint[key]
        if str(key).endswith("date") or str(key).endswith("time"):
            types.append("time")

        elif isfloat(item) or isint(item):
            types.append("number")

        # Python 3 string determination.
        elif isinstance(item, (str)):
            types.append("string")
        # Python 2.7 workaround to determine strings.
        # Basestring was deprecated in Python 3.
        else:
            try:
                if isinstance(item, basestring):
                    types.append("string")
            except TypeError:
                pass

    return types


def isfloat(value):
    try:
        number = float(value)
    except ValueError:
        return False
    else:
        return True


def isint(value):
    try:
        num_a = float(value)
        num_b = int(num_a)
    except ValueError:
        return False
    else:
        return num_a == num_b


def checkConsistency(input_data):
    """Checks the consistency of the dataset. Each item
	must contain the exact datapoint-type as the other."""
    if input_data:
        current = getDatapointTypes(input_data[0])
        for item in input_data[1:]:
            previous = current
            current = getDatapointTypes(item)
            if previous != current:
                return False
    return True

