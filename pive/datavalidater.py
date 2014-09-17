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

from collections import OrderedDict

def countKeys(raw_dataset):	
	"""Counts all keysets in the dataset."""
	keycount = {}
	for item in raw_dataset:
		try:	
			keyset = tuple(item.keys())
		except AttributeError as e:
			print ('Key counting failed. "%s" is not a key/value pair. Error: %s' % (item, e.args[0]))
			return {}
		else:
			# For each new keyset occurence,
			# generate the intial entry.		
			if (keyset not in keycount.keys()):		
				keycount[keyset] = 1			
			# For each known keyset increment the count.
			else:	
				keycount[keyset] += 1
	return keycount

def validateData(keyset_occurences):
	"""Checks the dataset for valid keysets. The last contained keyset
	with the most occurences will be assumed to be valid."""
	valid_tuple = ()
	validkeys = []
	maxcount = 0
	
	for key in list(keyset_occurences.keys()):		
		currentCount = keyset_occurences[key]
		if (currentCount >= maxcount):
			maxcount = currentCount
			valid_tuple = key
	#Return a valid keyset as list.
	for elem in valid_tuple:
		validkeys.append(elem)
	return validkeys
	
def generateValidDataset(valid_keyset, raw_dataset):
	"""Generates a valid dataset based on the highest count."""
	valid_data = []
	for item in raw_dataset:
		if valid_keyset == list(item.keys()):
			valid_data.append(item)
	return valid_data

def getAllKeysFromDataset(raw_dataset):
	"""Determines if there are keys shared by
	the whole dataset"""	
	allKeys = []
	for item in raw_dataset:
		for elem in list(item.keys()):
			if elem not in allKeys:
				allKeys.append(elem)
	return allKeys

def determineEvenKeyset(all_keys, raw_dataset):
	"""Determines if there are keys shared by
	the whole dataset."""	
	evenKeys = all_keys
	for item in raw_dataset:
		#Intersection of two lists.		
		evenKeys = list(set(evenKeys) & set(list(item.keys())))		
	return evenKeys

def generateValidDatasetFromEvenKeys(even_keyset, raw_dataset):
	"""Generates a valid dataset based on the keys shared by
	the whole dataset."""
	valid_data = []
	for item in raw_dataset:
		datapoint = OrderedDict({})
		for key in list(item.keys()):
			if key in even_keyset:
				datapoint[key] = item[key]
		if datapoint:
			valid_data.append(datapoint)
	return valid_data
