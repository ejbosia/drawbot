'''
Contour
This class has a list of Lines that make up the contour, and its heirarchy. the heirarchy determines if it is an inner or outer edge.

@author ejbosia
'''
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


import math
from geometry.line import Line
from geometry.point import Point


class Contour:

    def __init__(self, vertex_list):

        self.vertex_list = vertex_list

    # rotate all points in contour
    def rotate(self, angle):
        
        for i, _ in enumerate(self.vertex_list):
            self.vertex_list[i].rotate(angle)


    # find all intersections with the line
    def intersection(self, line):
        
        points = []

        next_p = self.vertex_list[1:] + self.vertex_list[0:1]

        for i, p in enumerate(self.vertex_list):

            temp = line.intersection(Line(p,next_p[i]))      

            if temp is None:
                continue
            else:
                points.append(temp)

        return points


    # return X and Y lists to plot
    def plot(self):

        # create the lists of points
        X = []
        Y = []

        for vertex in self.vertex_list:
            X.append(self.vertex.x)
            Y.append(self.vertex.y)

        return X,Y


    # return a string representation of the contour
    def __repr__(self):
        for vertex in self.vertex_list:
            output += str(vertex) + ","

        return output
