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

import jinja2
import os
import json
from pive.visualization import defaults as default
from pive.visualization import basevisualization as bv
from pive.visualization import viewportvisualization as vv


class Chart(bv.BaseVisualization, vv.ViewportVisualization):
    def __init__(self,
                 dataset,
                 template_name,
                 width=default.width,
                 height=default.height,
                 padding=default.padding,
                 viewport=default.viewport,
                 jumplength=default.jumplength):

        # Initializing the inherited pseudo-interfaces.
        bv.BaseVisualization.__init__(self)
        vv.ViewportVisualization.__init__(self)

        # Metadata
        self._title = 'barchart'
        self.__template_name = 'barchart'
        self.__dataset = dataset
        realpath = os.path.dirname(os.path.realpath(__file__))
        self.__template_url = '%s%s' % (realpath, default.template_path)
        self.__datakeys = []
        self.__version = default.p_version


        # Visualization properties.
        self.__width = width
        self.__height = height
        self.__padding = padding
        self.__viewport = viewport
        self.__jumplength = jumplength
        self.__xlabel = default.xlabel
        self.__ylabel = default.ylabel
        self.__label_size = default.label_size
        self.__threshold = default.threshold

        self.__iconwidth = default.iconwidth
        self.__iconheight = default.iconheight
        self.__iconcolor = default.iconcolor
        self.__iconhighlight = default.iconhighlight
        self.__colors = default.chartcolors

        # Axis properties.
        self.__shape_rendering = default.shape_rendering
        self.__line_stroke = default.line_stroke
        self.__font_size = default.font_size

        self.__barwidth = default.barwidth
        self.__verticalscale = 'linear'

    def set_title(self, title):
        self._title = title

    def set_threshold(self, threshold):
        self.__threshold = threshold

    def getViewport(self):
        return self.__viewport

    def set_labels(self, labels):
        self.__xlabel = labels[0]
        self.__ylabel = labels[1]

    def setDataKeys(self, datakeys):
        self.__datakeys = datakeys;

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

    def set_chart_colors(self, colors):
        """Basic Method."""
        self.__colors = colors

    def generate_visualization_dataset(self, dataset):
        """Basic Method."""
        visdataset = []

        for datapoint in dataset:
            visdatapoint = {}
            points = list(datapoint.keys())
            visdatapoint['value'] = datapoint[points[0]]
            visdatapoint['label'] = datapoint[points[1]]
            visdataset.append(visdatapoint)
        return visdataset

    def write_dataset_file(self, dataset, destination_url, filename):
        dest_file = '%s%s' % (destination_url, filename)
        outp = open(dest_file, 'w')
        json.dump(dataset, outp, indent=2)
        outp.close()
        print ('Writing: %s' % (dest_file))

    def setVerticalScale(self, scale):
        self.__verticalscale = scale

    def create_html(self, template):
        templateVars = {'t_title': self._title,
                        't_div_hook': self._div_hook}

        outputText = template.render(templateVars)
        return outputText

    def create_js(self, template, dataset_url):
        templateVars = {'t_width': self.__width,
                        't_height': self.__height,
                        't_padding': self.__padding,
                        't_viewport': self.__viewport,
                        't_jumplength': self.__jumplength,
                        't_xlabel': self.__xlabel,
                        't_ylabel': self.__ylabel,
                        't_iconwidth': self.__iconwidth,
                        't_iconheight': self.__iconheight,
                        't_iconcolor': self.__iconcolor,
                        't_iconhighlight': self.__iconhighlight,
                        't_datakeys': self.__datakeys,
                        't_url': dataset_url,
                        't_colors': self.__colors,
                        't_barwidth': self.__barwidth,
                        't_verticalscale': self.__verticalscale,
                        't_threshold' : self.__threshold,
                        't_div_hook': self._div_hook,
                        't_font_size': self.__font_size,
                        't_shape_rendering': self.__shape_rendering,
                        't_line_stroke': self.__line_stroke,
                        't_pive_version' : self.__version,
                        't_axis_label_size' : self.__label_size}

        outputText = template.render(templateVars)
        return outputText

    def write_file(self, output, destination_url, filename):

        dest_file = '%s%s' % (destination_url, filename)

        if not os.path.exists(destination_url):
            print ("Folder does not exist. Creating folder '%s'. " % (destination_url))
            os.makedirs(destination_url)

        f = open(dest_file, 'w')

        print ('Writing: %s' % (dest_file))

        for line in output:
            #f.write(line.encode('utf-8'))
            f.write(line)

        f.close()


    def get_js_code(self):
        dataset_url = '%s.json' % (self._title)
        js_template = self.load_template_file('%s%s.jinja' % (self.__template_url, self.__template_name))
        js = self.create_js(js_template, dataset_url)
        return js


    def get_json_dataset(self):
        return self.generate_visualization_dataset(self.__dataset)


    def create_visualization_files(self, destination_url):
        html_template = self.load_template_file('%shtml.jinja' % (self.__template_url))
        #css_template = self.load_template_file('%s/css.jinja' % (self.__template_url))
        js_template = self.load_template_file('%s%s.jinja' % (self.__template_url, self.__template_name))

        dataset_url = '%s.json' % (self._title)
        js = self.create_js(js_template, dataset_url)
        html = self.create_html(html_template)
        #css = self.create_css(css_template)

        self.write_file(html, destination_url, '/%s.html' % (self._title))
        #self.write_file(css, destination_url, '/%s.css' % (self.__title))
        self.write_file(js, destination_url, '/%s.js' % (self._title))

        visdata = self.generate_visualization_dataset(self.__dataset)
        self.write_dataset_file(visdata, destination_url, '/%s.json' % (self._title))

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

    def set_height(self, height):
        """Basic method for height driven data."""
        if not isinstance(height, int):
            raise ValueError("Integer expected, got %s instead." % (type(height)))
        if (height <= 0):
            print ("Warning: Negative or zero height parameter. Using default settings instead.")
            height = default.height
        self.__height = height

    def set_width(self, width):
        """Basic method for width driven data."""
        if not isinstance(width, int):
            raise ValueError("Integer expected, got %s instead." % (type(width)))
        if (width <= 0):
            print ("Warning: Negative or zero width parameter. Using default settings instead.")
            width = default.width
        self.__width = width

    def set_dimension(self, width, height):
        self.set_width(width)
        self.set_height(height)

    def load_template_file(self, template_url):
        templateLoader = jinja2.FileSystemLoader(searchpath=[default.template_path, '/'])
        print ("Opening template: %s" % (template_url))

        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = template_url
        template = templateEnv.get_template(TEMPLATE_FILE)
        return template
