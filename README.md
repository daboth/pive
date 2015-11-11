![pive Logo](/artwork/pive_logo_optimized_100x100.png)


Python Interactive Visualization Environment
=====

python-ive
[ˈpaiθən-ˈaivi]

(alternative titles: *p-ive* or preferably **pive**)

current version: 0.3.3

What is pive?

Pive is a template based visualization tool utilizing D3.js to create interactive visualizations on the fly. It is aimed
at users who want to enhance their web applications with dynamic D3.js visualizations without diving deep into the
coding of D3.js.

Install pive:

Clone this repository:
```
git clone https://github.com/daboth/pive.git
```
and install manually:
```
python setup.py install
```
or install with pip:
```
pip install pive
```

You may need to add ```sudo``` before executing each command.
Now write a simple script to render a chart:

```python

    #!/usr/bin/env python
    import pive.environment as environment
    import pive.inputmanager as inputmanager

	# Assuming you have a testdata.json file with some datapoints
	# in the same directory. Try to create JSON-Objekts as Key/Value
	# pairs or use a JSON formatted String Object. CSV is also
	# supported.
	input_path = 'samples/numerical.json'

	###########################
	### Basic usage of pive ###
	###########################
	# 1)Set up the environment by creating the input manager and
	# passing it to an environment. Optionally, you can omit
	# an output path. Default is 'output/'.
	manager = inputmanager.InputManager(mergedata=False)
	env = environment.Environment(inputmanager=manager)

	# 2) Load your dataset into the environment to get a
	# list of supported visualizations.
	supported = env.load(input_path)

	# 3) Check if your desired chart is in the list and choose
	# it as your visualization object. Alternatively you can
	# print out the list of the supported charts and choose directly
	# from it. The accessors, e.g. CHART_LINE, are environment
	# constants and represent the charts included in pive.
	if environment.CHART_LINE in supported:
	    chart = env.choose(CHART_LINE)

        #You can now edit the charts properties.
	    chart.set_width(900)
	    chart.set_height(500)

        # 4.1) Let the environment render the chart.
        # The visualizuation files will be generated
        # in the output path defined in the environment.
        env.render(chart)

        # 4.2) Optionally you can receive the
        # javascript code and its dataset as json.
        code = env.render_code(chart)
```
