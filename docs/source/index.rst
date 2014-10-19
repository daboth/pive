Python Interactive Visualization Environment
===============================================================================
python-ive
[ˈpaiθən-ˈaivi]

pive is a template based visualization tool utilizing d3.js_ to
create interactive visualizations on the fly. 

.. toctree::
   :maxdepth: 2


Quickstart:
^^^^^^^^^^^
Use this quickstart guide if you just want to have some data visualized without delving deeper into the structure of pive. The basic usage is explained here. For more information take a look at the full documentation.

Prepare by installing pive from your favorite source. It is recommended to install it through PIP_.
Make sure you install it for the python version you plan to use in your project.::
	
	pip install pive

For Python 3.0 and above install it with::
	
	pip3 install pive	

Begin by importing the pive environment and an input manager.::
	
	import pive.environment as env
	import pive.inputmanager as im


Assuming you have a testdata.json file with some datapoints
in the same directory. Try to create JSON-Objekts as Key/Value
pairs or use a JSON formatted String Object. CSV is also
supported.::

	input_path = 'testdata.json'

An example json data file may look like this::

	[
	    {
	        "x": 1,
	        "y1": 12,
	        "y2": 3
	    },
	    {
	        "x": 2,
	        "y1": 10,
	        "y2": 9
	    },
	    {
	        "x": 3,
	        "y1": 34,
	        "y2": 42
	    }
	] 

Set up the environment by creating the input manager and
passing it to an environment. The mergedata argument tells pive whether an invalid
should be merged into a new one with valid points or not.::

	manager = im.InputManager(mergedata=False)
	vizenv = environment.Environment(inputmanager=manager)



Load your dataset into the environment to get a
list of supported visualizations. You can print it out to see which
visualizations pive supports for this dataset.::

	suitable_charts = vizenv.load(input_path)
	print (suitable_charts)

Choose a chart from this list to manipulate
the visualization object. In this case, choose the first possible visualization.::

	mychart = vizenv.choose(suitable_charts[0])

Visualizations have specific and generic properties. Look into the documentation of each chart on how to use them.::

	mychart.setWidth(900)
	mychart.setHeight(500)

Let the environment render the chart. This generates all visualization files in the standard output path, which is /output.::

	vizenv.render(mychart)

	>Opening template: /templates///usr/local/lib/python2.7/dist-packages/pive/visualization/templates/linechart/html.jinja
	>Opening template: /templates///usr/local/lib/python2.7/dist-packages/pive/visualization/templates/linechart/css.jinja
	>Opening template: /templates///usr/local/lib/python2.7/dist-packages/pive/visualization/templates/linechart/js.jinja
	>Writing: /home/user/test/output/linechart.html
	>Writing: /home/user/test/output/linechart.css
	>Writing: /home/user/test/output/linechart.js
	>Writing: /home/user/test/output/linechart.json

To run your visualization make sure that your files run in a webserver environment. The visualization is based on the javascript library
d3.js_ and loads the datafile with a request. The python SimpleHTTPWebserver will do fine.::

	python -m SimpleHTTPServer

	>Serving HTTP on 0.0.0.0 port 8000 ...
 

This will start a simple webserver at the location you have invoked the command. Now navigate to 0.0.0.0:8000 in your browser (see the SimpleHTTPServer_ documentation for details) and view the beautiful visualization you (hopefully) just created.

.. _SimpleHTTPServer: https://docs.python.org/2/library/simplehttpserver.html
.. _d3.js: http://d3js.org
.. _PIP: https://pypi.python.org/pypi/pip


* :ref:`search`

