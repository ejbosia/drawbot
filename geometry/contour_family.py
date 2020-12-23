'''
Family
This holds a parent contour and its children.

@author ejbosia
'''

import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


import math
from geometry.line import Line


class Family:

    def __init__(self, parent_contour, children=[])
        self.parent_contour = parent_contour
        self.children = children

    # get the starting point to process the family
    def starting_point(self):
        pass


    def generate_intersection_points(self, starting_point, line_thickness, angle):



    # plot the family  
    def plot(self):
        pass