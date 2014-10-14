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


class Chart(bv.BaseVisualization):
    def __init__(self,
                 dataset,
                 template_name,
                 width=default.width,
                 height=default.height,
                 padding=default.padding):

        # Initializing the inherited pseudo-interfaces.
        bv.BaseVisualization.__init__(self)

        # Metadata
        self.__title = 'piechart'
        self.__dataset = dataset
        realpath = os.path.dirname(os.path.realpath(__file__))
        self.__template_url = '%s%s%s' % (realpath, default.template_path, template_name)
        self.__datakeys = []

        # Visualization properties.
        self.__width = width
        self.__height = height
        self.__padding = padding

        self.__colors = default.chartcolors

        self.__highlightopacity = default.circleopacity


    def setTitle(self, title):
        self.__title = title

    def setDataKeys(self, datakeys):
        self.__datakeys = datakeys

    def sethighlightOpacity(self, opacity):
        self.__highlightopacity = opacity

    def setChartColors(self, colors):
        """Basic Method."""
        self.__colors = colors

    def generateVisualizationDataset(self, dataset):
        """Basic Method."""
        visdataset = []

        for datapoint in dataset:
            visdatapoint = {}
            points = list(datapoint.keys())
            visdatapoint['value'] = datapoint[points[0]]
            visdatapoint['label'] = datapoint[points[1]]
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
        templateVars = {}
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
                        't_datakeys': self.__datakeys,
                        't_url': dataset_url,
                        't_colors': self.__colors,
                        't_highlightopacity': self.__highlightopacity}

        outputText = template.render(templateVars)
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

	

 