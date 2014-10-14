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

import jinja2
import os
import json
from pive.visualization import defaults as default
from pive.visualization import basevisualization as bv
from pive.visualization import viewportvisualization as vv
from pive.visualization import customscalesvisualization as csv


class Chart(bv.BaseVisualization, csv.CustomScalesVisualization, vv.ViewportVisualization):
    def __init__(self,
                 dataset,
                 template_name,
                 width=default.width,
                 height=default.height,
                 padding=default.padding,
                 viewport=default.viewport,
                 jumplength=default.jumplength,
                 times=False):

        # Initializing the inherited pseudo-interfaces.
        bv.BaseVisualization.__init__(self)
        csv.CustomScalesVisualization.__init__(self)
        vv.ViewportVisualization.__init__(self)
        realpath = os.path.dirname(os.path.realpath(__file__))

        # Metadata
        self.__title = 'scatterchart'
        self.__dataset = dataset
        self.__template_url = '%s%s%s' % (realpath, default.template_path, template_name)
        self.__datakeys = []

        # Visualization properties.
        self.__width = width
        self.__height = height
        self.__padding = padding
        self.__viewport = viewport
        self.__jumplength = jumplength
        self.__xlabel = default.xlabel
        self.__ylabel = default.ylabel

        if times:
            self.__scales = default.timescales
        else:
            self.__scales = default.scales

        self.__timelabel = default.timelabel
        self.__timeformat = default.isotimeformat
        self.__iconwidth = default.iconwidth
        self.__iconheight = default.iconheight
        self.__iconcolor = default.iconcolor
        self.__iconhighlight = default.iconhighlight
        self.__colors = default.chartcolors

        self.__circleradius = default.circleradius
        self.__circlehighlightradius = default.circlehighlightradius
        self.__circleopacity = default.circleopacity

        #Axis properties.
        self.__shape_rendering = default.shape_rendering
        self.__line_stroke = default.line_stroke
        self.__font_size = default.font_size

    def setTitle(self, title):
        self.__title = title

    def getViewport(self):
        return self.__viewport

    def setLabels(self, labels):
        self.__xlabel = labels[0]
        self.__ylabel = labels[1]

    def setDataKeys(self, datakeys):
        self.__datakeys = datakeys

    def setCircleOpacity(self, opacity):
        self.__circleopacity = opacity

    def setCircleRadius(self, radius):
        self.__circleradius = radius

    def setCircleHighlightRadius(self, radius):
        self.__circlehighlightradius = radius

    def setTimeProperties(self, timelabel, timeformat):
        """Basic Method for time supporting visualizations."""
        self.__timeformat = timeformat
        self.__timelabel = timelabel

    def setIconProperties(self, iconwidth, iconheight, iconcolor, iconhighlight):
        """Basic Method for viewport driven data.
		Defines the icon properties. All arguments required."""
        self.__iconwidth = iconwidth
        self.__iconheight = iconheight
        self.__iconcolor = iconcolor
        self.__iconhighlight = iconhighlight

    def setChartColors(self, colors):
        """Basic Method."""
        self.__colors = colors

    def generateVisualizationDataset(self, dataset):
        """Basic Method."""
        visdataset = []

        for datapoint in dataset:
            visdatapoint = {}
            points = list(datapoint.keys())
            visdatapoint['x'] = datapoint[points[0]]
            ordinates = []
            for item in points[1:]:
                ordinates.append(datapoint[item])
            visdatapoint['y'] = ordinates

            visdataset.append(visdatapoint)

        return visdataset

    def writeDatasetFile(self, dataset, destination_url, filename):
        dest_file = '%s%s' % (destination_url, filename)
        outp = open(dest_file, 'w')
        json.dump(dataset, outp, indent=2)
        outp.close()
        print ('Writing: %s' % (dest_file))

    def setScales(self, scales):
        self.__scales = scales

    def createCSS(self, template):
        templateVars = {'t_font_size': self.__font_size,
                        't_shape_rendering': self.__shape_rendering,
                        't_line_stroke': self.__line_stroke}

        outputText = template.render(templateVars)
        return outputText

    def createHTML(self, template):
        templateVars = {'t_title': self.__title}

        outputText = template.render(templateVars)
        return outputText

    def createJS(self, template, dataset_url):
        templateVars = {'t_width': self.__width,
                        't_height': self.__height,
                        't_padding': self.__padding,
                        't_viewport': self.__viewport,
                        't_jumplength': self.__jumplength,
                        't_xlabel': self.__xlabel,
                        't_ylabel': self.__ylabel,
                        't_timeformat': self.__timeformat,
                        't_iconwidth': self.__iconwidth,
                        't_iconheight': self.__iconheight,
                        't_iconcolor': self.__iconcolor,
                        't_iconhighlight': self.__iconhighlight,
                        't_datakeys': self.__datakeys,
                        't_url': dataset_url,
                        't_format': self.__timeformat,
                        't_iso': self.__timeformat,
                        't_scales': self.__scales,
                        't_colors': self.__colors,
                        't_circleradius': self.__circleradius,
                        't_highlightfactor': self.__circlehighlightradius,
                        't_circleopacity': self.__circleopacity}

        outputText = template.render(templateVars)
        print (self.__datakeys)
        return outputText

    def writeFile(self, output, destination_url, filename):

        dest_file = '%s%s' % (destination_url, filename)

        if not os.path.exists(destination_url):
            print ("Folder does not exist. Creating folder '%s'. " % (destination_url))
            os.makedirs(destination_url)

        f = open(dest_file, 'w')

        print ('Writing: %s' % (dest_file))

        for line in output:
            f.write(line)

        f.close()


    def createVisualizationFiles(self, destination_url):
        html_template = self.loadTemplate('%s/html.jinja' % (self.__template_url))
        css_template = self.loadTemplate('%s/css.jinja' % (self.__template_url))
        js_template = self.loadTemplate('%s/js.jinja' % (self.__template_url))

        dataset_url = '%s.json' % (self.__title)

        js = self.createJS(js_template, dataset_url)
        html = self.createHTML(html_template)
        css = self.createCSS(css_template)

        self.writeFile(html, destination_url, '/%s.html' % (self.__title))
        self.writeFile(css, destination_url, '/%s.css' % (self.__title))
        self.writeFile(js, destination_url, '/%s.js' % (self.__title))

        visdata = self.generateVisualizationDataset(self.__dataset)
        self.writeDatasetFile(visdata, destination_url, '/%s.json' % (self.__title))

    def setJumplength(self, jumplength):
        """Basic Method for viewport driven data."""
        if not isinstance(jumplength, int):
            raise ValueError("Integer expected, got %s instead." % (type(jumplength)))
        if (jumplength <= 0):
            print ("Warning: Negative or zero jumplength parameter. Using default settings instead.")
            jumplength = default.jumplength

        self.__jumplength = jumplength

    def setViewport(self, viewport):
        """Basic method for viewport driven data."""
        if not isinstance(viewport, int):
            raise ValueError("Integer expected, got %s instead." % (type(viewport)))
        if (viewport <= 0):
            print ("Warning: Negative or zero viewport parameter. Using default settings instead.")
            viewport = default.viewport
        self.__viewport = viewport

    def setHeight(self, height):
        """Basic method for height driven data."""
        if not isinstance(height, int):
            raise ValueError("Integer expected, got %s instead." % (type(height)))
        if (height <= 0):
            print ("Warning: Negative or zero height parameter. Using default settings instead.")
            height = default.height
        self.__height = height

    def setWidth(self, width):
        """Basic method for width driven data."""
        if not isinstance(width, int):
            raise ValueError("Integer expected, got %s instead." % (type(width)))
        if (width <= 0):
            print ("Warning: Negative or zero width parameter. Using default settings instead.")
            width = default.width
        self.__width = width

    def setDimension(self, width, height):
        self.setWidth(width)
        self.setHeight(height)

    def loadTemplate(self, template_url):
        templateLoader = jinja2.FileSystemLoader(searchpath=[default.template_path, '/'])
        print ("Opening template: %s/%s" % (default.template_path, template_url))

        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = template_url
        template = templateEnv.get_template(TEMPLATE_FILE)
        return template

	

 