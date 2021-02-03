'''
Line
This class represents a line (two points) or a ray (point and angle). Has logic to find intersections.

@author ejbosia
'''

import numpy as np
import math
import logging

from geometry.point import Point

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
        # check for parallel lines
        if((self.angle%np.pi) == (a%np.pi)):
            return False

        # create two temporary points for the line endpoints
        l1 = Point(self.p1.x, self.p1.y)
        l2 = Point(self.p2.x, self.p2.y)

        # move the points to 0
        l1.translate_XY(-p.x,-p.y)
        l2.translate_XY(-p.x,-p.y)

        # rotate the temp points to match the ray
        l1.rotate(-a)
        l2.rotate(-a)

        # if the sign of each y component are the same, intersection is impossible
        if(round(l1.y,10) * round(l2.y,10) > 0):
            return False

        '''
        X check
        - check the x normalized to y sum is greater than 0
        - the ray is currently at angle 0, so lines that have negative weight have an intersection point in -x
        '''

        if l1.y == 0:
            return l1.x > 0
        elif l2.y == 0:
            return l2.x > 0
        else:
            normal = l1.x/abs(l1.y) + l2.x/abs(l2.y)

            return normal > 0


    def intersection(self, line):

        check1 = self.check_possible_intersection(line.p1, line.angle)
        check2 = line.check_possible_intersection(self.p1, self.angle)

        if not check1 or not check2:
            return None
        
        s1 = np.tan(self.angle)
        s2 = np.tan(line.angle)

        V = (self.p1.y - line.p1.y + s1 * (line.p1.x - self.p1.x)) / (s2 - s1)

        px = line.p1.x + V
        py = line.p1.y + s2 * V

        return Point(px,py)



    
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
            X = [self.p1.x, self.p2.x]
            Y = [self.p1.y, self.p2.y]
            return X,Y

        else:
            raise Exception("NOT IMPLEMENTED YET")


    def __eq__(self, line):
        return line.p1 == self.p1 and line.p2 == self.p2

    def __repr__(self):
        return str(self.p1) + " - " + str(self.p2) + " ANGLE: " + str(round(self.angle,2))
