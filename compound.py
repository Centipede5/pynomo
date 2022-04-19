#!/usr/bin/python3

#nomogen example program

import sys

from nomogen import Nomogen
from pynomo.nomographer import Nomographer

########################################
#
#  this is the target function,
#  - the limits of the variables
#  - the function that the nonogram implements
#
#  format is m = m(l,r), where l, m & r are respectively the values
#                        for the left, middle & right hand scales
########################################

###################
# compound interest, epidemics, etc
def compound(r,y):
    # r = % rate pa, y = nr years
    i = r/100
    return (1 + i/365) ** (365*y)

imin = 1   ; imax = 5
ymin = 1   ; ymax = 10
wmin = compound(imin, ymin);
wmax = compound(imax, ymax);

###############################################################
#
# nr Chebychev nodes needed to define the scales
# a higher value may be necessary if the scales are very non-linear
# a lower value increases speed, makes a smoother curve, but could introduce errors

NN = 11

##############################################
#
# definitions for the scales for pyNomo
# dictionary with key:value pairs

  # the u scale
  # dictionary with key:value pairs
left_scale = {
    'u_min': imin,
    'u_max': imax,
    'title': r'$interest \thinspace rate$',
    'scale_type': 'linear smart',
    'tick_levels': 3,
    'tick_text_levels': 2,
    'grid': False
}

right_scale = {
    'u_min': ymin,
    'u_max': ymax,
    'title': r'$years$',
    'scale_type': 'linear smart',
    'tick_levels': 3,
    'tick_text_levels': 2,
    'grid': False
}

middle_scale = {
    'u_min': wmin,
    'u_max': wmax,
    'title': r'$final \thinspace value$',
    'scale_type': 'linear smart',
    'tick_levels': 3,
    'tick_text_levels': 2,
    'grid': False
}

block_params0 = {
    'block_type': 'type_9',
    'f1_params': left_scale,
    'f2_params': middle_scale,
    'f3_params': right_scale,
    'transform_ini': False,
    'isopleth_values': [[(imin+imax)/2, 'x', (ymin+ymax)/2]]
}

main_params = {
    'filename': __file__.endswith(".py") and __file__.replace(".py", ".pdf") or "nomogen.pdf",
    'paper_height': 10, # units are cm
    'paper_width': 10,
    'title_x': 5.0,
    'title_y': 1.0,
    'title_box_width': 8.0,
    'title_str':r'$final \thinspace value = (1 + {i \over 365}) ^ {365y}$',
    'block_params': [block_params0],
    'transformations': [('scale paper',)],
    'pdegree': NN
}

print("calculating the nomogram ...")
Nomogen(compound, main_params);  # generate nomogram for yrs function

print("printing ", main_params['filename'], " ...")
Nomographer(main_params);
