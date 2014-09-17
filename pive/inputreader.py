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
import csv
from collections import OrderedDict

def loadInputFile(input_source):
	"""Load data from an arbitrary input source. Currently supported:
	JSON, JSON-String, CSV, CSV-String. Returns an empty list if no data
	is available."""
	inputdata = []
	try:
		inputdata = loadJSON(input_source)
	except ValueError as e:
		pass
	except IOError as e:
		pass
	except Exception as e:
		pass
	else:
		return inputdata
		
	if not inputdata:
		try:
			inputdata = loadJSONString(input_source)
		except AttributeError as e:
			pass
		except ValueError as e:
			pass
		except Exception as e:
			pass
	
	if not inputdata:
		try:
			inputdata = loadCSV(input_source)
		except csv.Error as e:
			pass
		except IOError as e:
			pass
		except Exception as e:
			pass

	if  not inputdata:
		try:
			inputdata = loadCSVString(input_source)
		except Exception as e:
			pass
	return inputdata

def loadJSON(json_input):
	"""Load a JSON File."""
	fp = open(json_input, 'r')
	inpt = json.load(fp, object_pairs_hook=OrderedDict)
	return inpt

def loadJSONString(json_input):
	"""Load a JSON-String."""
	inpt = json.loads(json_input, object_pairs_hook=OrderedDict)
	return inpt

def loadCSVString(csv_input):
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
			value = parseValueType(row[item])
			od[item] = value
		data.append(od)

	return data

def UnicodeDictReader(utf8, **kwargs):
	"""Generator for unicode csv dictionary proccessing."""
	unic_reader = csv.DictReader(utf8, **kwargs)
	for row in unic_reader:
		yield OrderedDict([(key, unicode(value, 'utf-8')) for key, value in row.iteritems()])


def loadCSV(csv_input):
	"""Loads the input from a csv file and returns
	a list of ordered dictionaries for further processing."""
	data = []
	csvfile = open(csv_input)
	csvfile.seek(0)
	dialect = csv.Sniffer().sniff(csvfile.read())
	csvfile.seek(0)
	isHeader = csv.Sniffer().has_header(csvfile.read())
	csvfile.seek(0)
    #The delimiter used in the dialect.
	delimiterchar = dialect.delimiter
    #Opens the input file with the determined delimiter.
	dictreader = csv.DictReader(csvfile, dialect=dialect)
	
	header = dictreader.fieldnames

    #Translate the data into a list of dictionaries.
	for row in dictreader:

		od = OrderedDict()
		for item in header:
			value = parseValueType(row[item])

			od[item] = value

		data.append(od)  
	return data

def parseValueType(value):
	if isint(value):
		value = int(value)
	elif isfloat(value):
		value = float(value)
	return value

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


def loadCSV1(csv_input):
	"""Loads the input from a csv file and returns
	a list of ordered dictionaries for further processing."""
	data = []
	print ("data = []")
	print ("Input: ", csv_input)

	#Determines the dialect used in the input file.
	dialect = csv.Sniffer().sniff(open(csv_input).read())
	isHeader = csv.Sniffer().has_header(open(csv_input).read())

	#Try to open the CSV File.
	with open(csv_input, 'rb') as csvfile:
		line = csvfile.read()
	    #Resets the cursor position in the input file.
		csvfile.seek(0)
	    #Opens the input file with the determined delimiter.
		dictreader = csv.DictReader(csvfile, dialect=dialect)
		for row in dictreader:
			print (row)

	    #Translate the data into a list of dictionaries.
		for row in dictreader:
			data.append(OrderedDict([(key, unicode(value, 'utf-8')) for key, value in row.iteritems()]))	   
	return data
