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
        if self.length() >= temp.length():
            return True
        else:
            return False

    # find the intersection point with another line ~ None if there is none
    def intersection(self, line):
        
        # check if the angles are the same
        if (self.angle - line.angle) % 180 == 0:
            return None

        # find the intersection point
        point = self.__intersection_ray(line)

        # check if the point is on the line
        if self.check_on_line(point):
            return point
        
        else:
            return None

    # find the intersection point of the two lines, treated as rays
    def __intersection_ray(self, line):
        # Px + dx * U = lx + dlx * V
        # Py + dy * U = ly + dly * V

        '''
        dx, dy = self.slope()
        lx, ly = line.slope()

        self.p1[0] + dx * U = line.p1[0] + lx * V
        self.p1[1] + dy * U = line.p1[1] + ly * V

        U = ((line.p1[0] + lx * V - self.p1[0]) / dx)

        self.p1[1] + dy * U = line.p1[1] + ly * V

        self.p1[1]  - line.p1[1] = ly * V - dy * U 
        self.p1[1] - line.p1[1] + (dy/dx) * (line.p1[0] - self.p1[0]) = (ly - (dy/dx) * lx) * V 
        '''
        dx, dy = self.slope()
        lx, ly = line.slope()

        V = (self.p1[1] - line.p1[1] + (dy/dx) * (line.p1[0] - self.p1[0])) / (ly - (dy/dx) * lx)

        px = line.p1[0] + lx * V
        py = line.p1[1] + ly * V
        return (px, py)


    def length(self):
        if self.p2 is None:
            return np.inf

        dx,dy = self.slope()

        return math.sqrt(dx**2 + dy**2)
    
        
    def __eq__(self, line):
        return line.p1 == p1 and line.p2 == p2

    def __repr__(self):
        return str(p1) + " - " + str(p2)
