'''
Line
This class represents a line (two points) or a ray (point and angle). Has logic to find intersections.

@author ejbosia
'''

import numpy as np
import math
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

class Line:

    def __init__(self, p1, p2=None, angle=None):
        
        self.p1 = p1

        if p2 is None and angle is None:
            raise Exception("P2 or Angle required")
        
        self.p2 = p2

        if angle is None:
            self.angle = self.__angle()
        else:
            self.angle = angle


    # find the angle of the line from p1 to p2
    def __angle(self):
        dx = self.p2.x - self.p1.x
        dy = self.p2.y - self.p1.y
        return np.arctan2(dy,dx)


    # find the slope of the line (dy/dx)
    def slope(self):

        dx = math.cos(self.angle)
        dy = math.sin(self.angle)

        return dx,dy


    # find the point at the center of the line
    def bisect(self):
        
        if self.p2 is None:
            return None

        x = (self.p1.x + self.p2.x)/2
        y = (self.p1.y + self.p2.y)/2

        return (x,y)


    # find the length of the line (ray has an infinite length)
    def length(self):
        if self.p2 is None:
            return np.inf

        dx = self.p2.x - self.p1.x
        dy = self.p2.y - self.p1.y

        return math.sqrt(dx**2 + dy**2)


    # traverse the line a distance from p1
    def traverse(self, distance):

        if distance > self.length():
            raise Exception("TRAVERSE TOO LONG")

        ux, uy = self.slope()

        px = distance * ux + self.p1.x
        py = distance * uy + self.p1.y

        return (px, py)

    '''
    Check if there is a possible intersection
    '''
    def check_possible_intersection(self, p, a):
        # create two temporary points for the line endpoints
        l1 = self.p1
        l2 = self.p2

        # move the points to 0
        l1.translate(-p.x,-p.y)
        l2.translate(-p.x,-p.y)

        # rotate the temp points to match the ray
        l1.rotate(-a)
        l2.rotate(-a)

        # if the sign of each y component are the same, intersection is impossible
        if(l1.y * l2.y > 0):
            return False

        '''
        X check
        - check the x normalized to y sum is greater than 0
        - the ray is currently at angle 0, so lines that have negative weight have an intersection point in -x
        '''
        normal = l1.x/abs(l1.y) + l2.x/abs(l2.y)

        return normal > 0


    
    # return the cross product of this and another line
    def cross_product(self, line):

        ax = self.p2.x-self.p1.x
        ay = self.p2.y-self.p1.y

        bx = line.p2.x-line.p1.x
        by = line.p2.y-line.p1.y

        result = (ax * by) - (ay*bx)

        return result
    
    # return a zip of the line for plotting
    def plot(self):
        
        if not self.p2 is None:
            points = [self.p1, self.p2]
    
        else:
            dx, dy = self.slope()
            points = [self.p1, (dx*40+self.p1.x, dy*40+self.p1.y)]

        return zip(*points)


    def __eq__(self, line):
        return line.p1 == self.p1 and line.p2 == self.p2

    def __repr__(self):
        return str(self.p1) + " - " + str(self.p2) + " ANGLE: " + str(round(self.angle,2))
