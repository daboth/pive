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
from . import defaults as default
from abc import ABCMeta, abstractmethod
import jinja2
import os
import json

class BaseVisualization:
    __metaclass__ = ABCMeta
    implErrorMessage = 'Function not yet implemented.'

    def __init__(self):
        self._div_hook = default.div_hook
        self._template_url = ''
        self._template_name = ''
        self._dataset_url = ''
        self.dataset = []
        self._title = ''

    def set_div_hook(self, div_hook):
        assert isinstance(div_hook, str)
        self._div_hook = div_hook

    def get_js_code(self):
        js_template = self.load_template_file('%s%s.jinja' % (self._template_url, self._template_name))
        js = self.create_js(js_template, self._dataset_url)
        return js

    def get_json_dataset(self):
        return self.generate_visualization_dataset(self._dataset)

    def set_title(self, title):
        assert isinstance(title, str)
        self._title = title

    def set_labels(self, labels):
        raise NotImplementedError(self.implErrorMessage)

    def set_dataset(self, dataset):
        raise NotImplementedError(self.implErrorMessage)

    def set_dataset_url(self, dataset_url):
        assert isinstance(dataset_url, str)
        self._dataset_url = dataset_url

    def set_chart_colors(self, colors):
        """Basic Method."""
        self.__colors = colors

    @abstractmethod
    def generate_visualization_dataset(self, dataset):
        return


    def write_dataset_file(self, dataset, dataset_url):
        outp = open(dataset_url, 'w')
        json.dump(dataset, outp, indent=2)
        outp.close()
        print ('Writing: %s' % (dataset_url))


    def create_html(self, template):
        templateVars = {'t_title': self._title,
                        't_div_hook': self._div_hook}

        outputText = template.render(templateVars)
        return outputText

    @abstractmethod
    def create_js(self, template, dataset_url):
        return

    def write_file(self, output, destination_url, filename):

        dest_file = '%s%s' % (destination_url, filename)

        if not os.path.exists(destination_url):
            print ("Folder does not exist. Creating folder '%s'. " % (destination_url))
            os.makedirs(destination_url)

        f = open(dest_file, 'w')

        print ('Writing: %s' % (dest_file))

        for line in output:
            f.write(line)

        f.close()

    def create_visualization_files(self, destination_url):

        html_template = self.load_template_file('%shtml.jinja' % (self._template_url))
        js_template = self.load_template_file('%s%s.jinja' % (self._template_url, self._template_name))
        print "What"

        # Default dataset url is used when nothing was explicitly passed.
        if not self._dataset_url:
            dataset_url = destination_url + '%s%s.json' % (os.sep, self._title)
            self.set_dataset_url(dataset_url)
            # By default, the dataset is stored directly in the visualizations javascript path,
            # the templating engine then only references the relative path.
            js = self.create_js(js_template, '%s.json' % (self._title))
        else:
            # When a dataset url was passed, the visualization references
            # this as the absolute path to the dataset.
            js = self.create_js(js_template, self._dataset_url)

        html = self.create_html(html_template)

        self.write_file(html, destination_url, '%s%s.html' % (os.sep, self._title))
        self.write_file(js, destination_url, '%s%s.js' % (os.sep, self._title))

        visdata = self.generate_visualization_dataset(self._dataset)
        self.write_dataset_file(visdata, self._dataset_url)

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
        path, filename = os.path.split(template_url)
        template_loader = jinja2.FileSystemLoader(searchpath=[path, './'])
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template(filename)
        return template
