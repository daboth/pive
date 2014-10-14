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

from pive.visualization import colorthemes
import sys

####################
## Meta Data #######
####################
title = 'pivechart'
# Used to locate the modules with dotted namespace.
module_path = 'pive.visualization'
# Filepath to the template folder.
template_path = '/templates/'
# Path where pive will create the standard output.
output_path = '%s/output' % (sys.path[0])
# Path where pive locates the visualizations config file.
config_path = '/visualization/config/'

####################
## Default Values ##
####################
width = 900
height = 600
padding = 60
viewport = 50
jumplength = 10
iconwidth = 20
iconheight = 40
circleradius = 8
circlehighlightradius = 12
circleopacity = 0.5
highlightfactor = 1.1
minradius = 1
maxradius = 50
barwidth = 20

####################
## Axis Rendering ##
####################
shape_rendering = 'optimizeSpeed'
line_stroke = 'black'
font_size = 16

####################
## Formatting ######
####################
timelabel = '%M %S Sek'
isotimeformat = "%H:%M:%S"
interpolation = 'linear'
scales = ["linear", "linear"]
timescales = ["date", "linear"]
xlabel = 'X'
ylabel = 'Y'

##########################
## Chord Chart specific ##
##########################
fontsize = '1.25em'
ticksize = '.75em"'
textpadding = 45
#Defaults go for kilo-steps (K, 1000). Always combine them right.
ticksteps = 1000
prefix = 'K'

####################
## Colors ##########
####################
iconcolor = '#FF2C00'
iconhighlight = '#FF8B73'
chartcolors = colorthemes.pive_theme

