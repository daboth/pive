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

import sys
import importlib
from .visualization import defaults as default



# Bundles all essential access methods to render visualizations.
class Environment():
    # Contains all suitable visualizations. Only those
    # visualizations are imported and it is not
    # allowed to render unsuited visualizations.
    __suitables = []
    __data = []

    # The acual visualization modules.
    __modules = []

    __hasDates = False

    __datakeys = []

    # The Environment needs an input manager instance to work, but is optional
    # at creation. Leaving the user to configure the input manager first.
    def __init__(self, inputmanager=None, outputpath=default.output_path):
        self.__inputmanager = inputmanager
        self.__outputpath = outputpath

    # Set the output path of all visualization files.
    def setOutputPath(outputpath):
        self.__outputpath = outputpath

    # Change the internal input manager instance
    def setInputManager(self, inputmanager):
        self.__inputmanager = inputmanager

    # Load the dataset utilizing the internal input manager.
    def load(self, source):
        """Loads data from a source."""
        inputdata = self.__inputmanager.read(source)
        self.__suitables = self.__inputmanager.map(inputdata)
        self.__modules = self.importSuitableVisualizations(self.__suitables)
        self.__data = inputdata
        self.__hasDates = self.__inputmanager.hasDatePoints()
        # Converting the datakeys into strings.
        self.__datakeys = [str(i) for i in list(self.__data[0].keys())]
        return self.__suitables

    # Import all visualization modules.
    def importSuitableVisualizations(self, suitables):
        """Dynamically import all suited visualization files."""

        mods = []
        for item in suitables:
            mod = '.%s' % item
            mods.append(mod)

        modules = []

        for item in mods:
            modules.append(importlib.import_module(item, package=default.module_path))

        return modules

    # Choose a chart to start modifying or render it.
    def choose(self, chart):
        """Choose a chart from the suitable visualizations."""
        if chart not in self.__suitables:
            raise ValueError("Visualization not allowed.")

        # Automatically create the chart instance and
        # return it to the user.
        index = self.__suitables.index(chart)
        modname = self.__suitables[index]
        module = self.__modules[index]

        class_ = getattr(module, "Chart")

        # When dates occur the constructor is called differently.
        if (self.__hasDates):
            mychart = class_(self.__data, modname, times=True)
        else:
            mychart = class_(self.__data, modname)

        mychart.setDataKeys(self.__datakeys)
        return mychart

    # Render the chart by creating all visualization files.
    def render(self, chart):
        """Render the chart."""
        chart.createVisualizationFiles(self.__outputpath)