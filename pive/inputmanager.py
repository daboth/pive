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

from . import inputreader as reader
from . import datavalidater as validater
from . import consistenceprofiler as profiler
from . import visualizationmapper as vizmapper

notConsistentErrorMsg = "Data is not consistent."

class InputManager:
	
	# Input Managers can try to merge false datapoints or not.
	def __init__(self, mergedata=False):		
		self.__mergedata = mergedata
		self.__containsDates = False

	def read(self, source):
		"""Reads the input source."""
		inputdata = reader.loadInputFile(source)
		dataset = self.__validateInput(inputdata)
		if not self.__checkConsistency(dataset):
			raise ValueError (notConsistentErrorMsg)
		return dataset

	def map(self, dataset):
		"""Maps the dataset to supported visualizations."""
		viztypes = self.__getVisualizationTypes(dataset)
		properties = vizmapper.getVisualizationProperties(dataset, viztypes)
		suitables = vizmapper.checkPossibilities(properties)
		self.__containsDates = vizmapper.hasDate(viztypes)
		return suitables

	def hasDatePoints(self):
		"""Returns true if the data contains dates."""
		return self.__containsDates

	def __checkConsistency(self, dataset):
		"""Checks if the dataset is consistent."""
		consistent = profiler.checkConsistency(dataset)
		return consistent

	def __getVisualizationTypes(self, dataset):
		"""Returns all containing visualization types."""
		viztypes = profiler.getDatapointTypes(dataset[0])
		return viztypes

	def __validateInput(self, inputdata):
		"""Validates the input data:"""
		validdata = []
		if self.__mergedata:
			validdata = self.__mergedDatasetValidation(inputdata)
		else:
			validdata = self.__datasetValidation(inputdata)
		return validdata

	def __mergedDatasetValidation(self, inputdata):
		"""Validate the data by merging all shared keys."""
		allkeys = validater.getAllKeysFromDataset(inputdata)
		sharedkeys = validater.determineEvenKeyset(allkeys, inputdata)
		dataset = validater.generateValidDatasetFromEvenKeys(sharedkeys, inputdata)
		return dataset

	def __datasetValidation(self, inputdata):
		"""Validate the unmerged data by counting the keys."""
		keycount = validater.countKeys(inputdata)
		validkeys = validater.validateData(keycount)
		dataset = validater.generateValidDataset(validkeys, inputdata)
		return dataset

