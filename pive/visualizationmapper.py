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

import json
from glob import glob
from collections import OrderedDict
from .visualization import defaults as default
import os

config_path = default.config_path
# The directory in which pive was installed.
realpath = os.path.dirname(os.path.realpath(__file__))
internal_config_path = '%s%s' % (realpath, config_path)

def openConfigFiles(default_config_path):
    """Opens all json-config files in a directory and
	returns a list of each files content."""
    configs = []
    for filename in glob(internal_config_path + '*.json'):
        fp = open(filename, 'r')
        conf = json.load(fp, object_pairs_hook=OrderedDict)
        configs.append(conf)
    return configs


def hasDate(viz_types):
    """Checks if the datapoint has dates."""
    times = False
    for item in viz_types:
        if item == 'time':
            times = True
    return times


def getVisualizationProperties(dataset, viz_types):
    """Generates a list of the dataset properties. Returns
	all properties in the following order: Number of Datapoints,
	Number of Variables, Datesupport,
	List of Visualization-Types."""
    props = []
    length = len(dataset)
    props.append(length)
    props.append(len(viz_types))
    times = hasDate(viz_types)
    props.append(times)
    props.append(viz_types)

    # Indicates, if the abcissa of the dataset is in lexicographic order.
    if ((viz_types[0] in ('number', 'time')) and length > 1):
        lexicographic = isInLexicographicOrder(dataset)
    else:
        lexicographic = False

    props.append(lexicographic)
    return props


def matchesDataRequirements(given_types, required_types):
    """Verifies if all given types match the requirements.
	Requirements may vary and support multiple options."""
    matches = True
    i = 0

    for item in given_types:
        print ("item: %r     req: %r" % (item, required_types[i]))

        if item not in required_types[i]:
            matches = False
        i += 1
    return matches


def multiDataConsistent(given_types, singleDataLength):
    """Verifies if the multiple data elements following
	the last single data element are consistent."""
    consistent = True
    last_index = singleDataLength - 1
    last_element = given_types[last_index]

    for item in given_types[last_index:]:
        if item != last_element:
            consistent = False
    return consistent


def isAscending(dataset):
    """Checks if the data is ascending."""
    ascending = True
    starting_abscissa = list((dataset[0]).items())[0][1]
    last_abscissa = starting_abscissa
    for item in dataset[1:]:
        current_abscisssa = list(item.items())[0]
        if (current_abscisssa[1] <= last_abscissa):
            ascending = False
        last_abscissa = current_abscisssa[1]
    return ascending


def isDescending(dataset):
    """Checks if the data ist descending."""
    descending = True
    starting_abscissa = list((dataset[0]).items())[0][1]
    last_abscissa = starting_abscissa
    for item in dataset[1:]:
        current_abscisssa = list(item.items())[0]
        if (current_abscisssa[1] >= last_abscissa):
            descending = False
        last_abscissa = current_abscisssa[1]
    return descending


def isInLexicographicOrder(dataset):
    """Checks if the data is ascending or descending."""
    lexicographic = True
    if not (isDescending(dataset) or isAscending(dataset)):
        lexicographic = False
    return lexicographic


def checkPossibilities(property_list):
    """Checks if the input data maps to any of
	the visualization configs and returns a resultlist
	with the supported charts."""
    result = []
    props = property_list
    conf = openConfigFiles(config_path)

    for item in conf:
        item_type = item['title']
        isPossible = True
        supportsMultiData = False

        for elem in item.keys():
            # The dataset should contain at
            #least the minimum required datapoints.
            if elem == 'min_datapoints':
                if props[0] < item[elem]:
                    isPossible = False
            #The dataset should not contain more
            #than the maximum number off supported
            #datapoints.
            if elem == 'max_datapoints':
                if item[elem] != 'inf':
                    if (props[0] > item[elem]):
                        isPossible = False

            #If the data contains a date, the visualization
            #has to support date-types.
            if elem == 'datesupport':
                if props[2]:
                    if item[elem] != props[2]:
                        isPossible = False
            if elem == 'multiple_data':
                supportsMultiData = item[elem]

            if elem == 'lexical_required':
                if item[elem] == True:
                    if not props[4]:
                        isPossible = False

            #Checks if the input order of the desired viz-types matches
            #the requirements.
            if ((elem == 'vistypes') and isPossible):
                isPossible = checkInputOrder(elem, item, props, supportsMultiData)
        if isPossible:
            result.append(item_type)
    return result


def checkInputOrder(elem, item, props, supportsMultiData):
    """Checks if the input vistypes match the requirements."""
    isPossible = True
    req_vtypes = []
    for i in item[elem]:
        for j in i:
            req_vtypes.append(i[j])

    # Length required to render a single dataset.
    singleDataLength = len(req_vtypes)

    eachValCount = len(req_vtypes) - 1
    dataValCount = len(props[3]) - 1
    if ((dataValCount % eachValCount) != 0):
        isPossible = False

    for item in props[3]:
        print (item)
        str(item)
        print (item)

    # Determines the given types.
    if (len(props[3]) >= singleDataLength):
        given_types = props[3][:singleDataLength]
    else:
        given_types = props[3]

    datalength = len(props[3])
    requiredlength = len(req_vtypes)

    # If the data is larger than the single length it must match the
    # requirements for multiple datasets.
    data_matches = matchesDataRequirements(given_types, req_vtypes)

    if not data_matches:
        isPossible = False

    if (datalength > requiredlength):
        if supportsMultiData:
            # All points in multiple datasets must be consistent.
            multi_consistent = multiDataConsistent(given_types, singleDataLength)
            if not multi_consistent:
                isPossible = False
        else:
            isPossible = False
    elif (datalength < requiredlength):
        isPossible = False

    return isPossible