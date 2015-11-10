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

# -*- coding: utf-8 -*-
""" The input manager reads files and strings containing
datasets in json and csv format. The data is automatically
validated and corrected if necessary."""
from . import inputreader as reader
from . import datavalidater as validater
from . import consistenceprofiler as profiler
from . import visualizationmapper as vizmapper

NOT_CONSISTENT_ERR_MSG = "Data is not consistent."
NO_DATA_LOADED_ERR_MSG = "Unexpected data source."


class InputManager(object):
    """Contains and manages the data."""

    # Input Managers can try to merge false datapoints or not.
    def __init__(self, mergedata=False):
        self.__mergedata = mergedata
        self.__contains_datefields = False

    def read(self, source):
        """Reads the input source."""
        inputdata = reader.load_input_source(source)

        # Raise an error if the data source is empty or nor readable.
        if not inputdata:
            raise ValueError(NO_DATA_LOADED_ERR_MSG)

        dataset = self.__validate_input(inputdata)
        # Raise an error if the dataset is not consistent.
        if not self.__is_dataset_consistent(dataset):
            raise ValueError(NOT_CONSISTENT_ERR_MSG)

        return dataset

    def map(self, dataset):
        """Maps the dataset to supported visualizations."""
        viztypes = self.__get_datapoint_types(dataset)
        properties = vizmapper.get_visualization_properties(dataset, viztypes)
        suitables = vizmapper.check_possibilities(properties)
        self.__contains_datefields = vizmapper.has_date(viztypes)
        return suitables

    def has_date_points(self):
        """Returns true if the data contains dates."""
        return self.__contains_datefields

    def __is_dataset_consistent(self, dataset):
        """Checks if the dataset is consistent."""
        consistent = profiler.is_dataset_consistent(dataset)
        return consistent

    def __get_datapoint_types(self, dataset):
        """Returns all containing visualization types."""
        viztypes = profiler.get_datapoint_types(dataset[0])
        return viztypes

    def __validate_input(self, inputdata):
        """Validates the input data:"""
        validdata = []
        if self.__mergedata:
            validdata = self.__merged_dataset_validation(inputdata)
        else:
            validdata = self.__dataset_validation(inputdata)
        return validdata

    def __merged_dataset_validation(self, inputdata):
        """Validate the data by merging all shared keys."""
        allkeys = validater.get_all_keys_in_dataset(inputdata)
        sharedkeys = validater.determine_shared_keys_in_dataset(allkeys,
                                                                inputdata)
        dataset = validater.generate_valid_dataset_from_shared_keys(sharedkeys,
                                                                    inputdata)
        return dataset

    def __dataset_validation(self, inputdata):
        """Validate the unmerged data by counting the keys."""
        keycount = validater.count_keys_in_raw_data(inputdata)
        validkeys = validater.validate_data_keys(keycount)
        dataset = validater.generate_valid_dataset(validkeys, inputdata)
        return dataset

