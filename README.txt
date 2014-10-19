=========
Python Interactive Visualization Environment
=========

Pive is a template based visualization tool utilizing D3.js to
create interactive visualizations on the fly. 

(alternative titles: *p-ive* or preferably **pive**)

python-ive
[ˈpaiθən-ˈaivi]

current version: 0.2.2


Common usage is shown in an example:

    #!/usr/bin/env python
	import pive.environment as environment # Modify to pive-path.
	from pive import inputmanager as im # Modify to pive-path.

	# Assuming you have a testdata.json file with some datapoints
	# in the same directory. Try to create JSON-Objekts as Key/Value
	# pairs or use a JSON formatted String Object. CSV is also
	# supported.
	input_path = 'testdata.json' 

	###########################
	### Basic usage of pive ###
	###########################
	# 1)Set up the environment by creating the input manager and
	# passing it to an environment.
	manager = im.InputManager(mergedata=False)
	vizenv = environment.Environment(inputmanager=manager)

	# 2) Load your dataset into the environment to get a
	# list of supported visualizations.
	suitable_charts = vizenv.load(input_path)


	# 3) Choose a chart from this list and manipulate
	# the visualization object.
	mychart = vizenv.choose(suitable_charts[0])

	mychart.setWidth(900)
	mychart.setHeight(500)

	# 4) Let the environment render the chart.
	vizenv.render(mychart)


For more information visit `<https://github.com/daboth/pive>`.