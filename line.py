'''
Line
This class represents a line (two points) or a ray (point and angle). Has logic to find intersections.

@author ejbosia
'''

import numpy as np
import math

class Line:

    def init(self, p1, p2=None, angle=None):
        self.p1 = p1
        if p2 is None and angle is None:
            raise Exception("P2 or Angle required")
        
        self.p2 = p2

        if angle is None:
            self.angle = self.angle()
        else:
            self.angle = angle


    # find the angle of the line from p1 to p2
    def angle(self):
        dx, dy = self.slope()
        return np.arctan(dy/dx)

    # find the slope of the line (dy/dx)
    def slope(self):
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        
        return dx,dy

    # check if the input point is on the line
    def check_on_line(self, point):

        # build a temporary line from p1 to the input point
        # TODO this might not be the most efficient method
        temp = Line(self.p1, p2=point)

        # if the angle is not equivalent, return false
        if not self.angle == temp.angle
            return False

        # to be on the line, the point must be between the two existing points
        if self.length >= temp.length:
            return True
        else:
            return False

    # find the intersection point with another line ~ None if there is none
    def intersection(self, line):
        
        # check if the angles are the same
        if (self.angle - line.angle) % 180 == 0:
            return None

        # find the intersection point


        # check if the point is on the line


    def length(self):
        if self.p2 is None:
            return np.inf

        dx,dy = self.slope()

        return math.sqrt(dx**2 + dy**2)
        

    # compare the lengths of the lines
    def __le__(self,other):
        return(self.seq<=other)
        
    def __eq__(self, line):
        return line.p1 == p1 and line.p2 == p2

    def __repr__(self):
        return str(p1) + " - " + str(p2)
