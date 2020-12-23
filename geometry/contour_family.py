'''
Family
This holds a parent contour and its children.

@author ejbosia
'''

import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


import math
import numpy as np
import matplotlib.pyplot as plt


from geometry.line import Line
from geometry.contour import Contour
from geometry.point import Point


class Family:

    def __init__(self, parent_contour, children=[]):
        self.parent_contour = parent_contour
        self.children = children

    # get the starting point to process the family
    def __starting_point(self, angle):
        return self.parent_contour.find_maximum_point(angle-(np.pi/2))

    # get all of the intersections of a line on the family
    def intersection(self, line):

        intersections = self.parent_contour.intersection(line)

        for child_contour in self.children:
            intersections.extend(child_contour.intersection(line))

        return intersections

    # generate the intersection points on each contour in the family
    def generate_intersection_points(self, line_thickness, angle):

        current_point = self.__starting_point(angle)

        # generate inifinite lines starting from the starting point + line_thickness perpendicular to the angle
        # the infinite lines comprise of two rays with directions of angle and angle + pi
        # once a "no intersection" point is reached (for both rays), the process stops

        # start the loop
        intersections = True

        perpendicular_angle = angle + (np.pi/2)

        rows = []

        # loop until there are no intersections
        while intersections:
            
            points = []

            # generate a new line
            dx = np.cos(perpendicular_angle)
            dy = np.sin(perpendicular_angle)

            current_point = (dx*line_thickness+current_point[0], dy*line_thickness+current_point[1])

            ray1 = Line(current_point, angle=angle)
            ray2 = Line(current_point, angle=angle-np.pi)

            # check the line for intersections against the parent and all children
            intersections = self.intersection(ray1)
            intersections.extend(self.intersection(ray2))

            # add the points
            for point in intersections:
                points.append(Point(point[0],point[1]))

            # if there are no points to add, do not create a new row
            if points:
                rows.append(np.sort(points))    

        # plot the rows
        for row in rows:  
            X = []
            Y = []

            for point in row:
                X.append(point.x)
                Y.append(point.y)

            plt.scatter(X,Y)

        self.plot()
        plt.show()

        return rows


    # plot the family  
    def plot(self, show=False):

        X,Y = self.parent_contour.plot()

        plt.plot(X,Y)
        
        for child_contour in self.children:
            
            X,Y = child_contour.plot()
            plt.plot(X,Y)
        
        if show:
            plt.show()
        
