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
        dx = self.p2[0] - self.p1[0]
        dy = self.p2[1] - self.p1[1]
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

        x = (self.p1[0] + self.p2[0])/2
        y = (self.p1[1] + self.p2[1])/2

        return (x,y)


    # find the length of the line (ray has an infinite length)
    def length(self):
        if self.p2 is None:
            return np.inf

        dx = self.p2[0] - self.p1[0]
        dy = self.p2[1] - self.p1[1]

        return math.sqrt(dx**2 + dy**2)


    # traverse the line a distance from p1
    def traverse(self, distance):

        if distance > self.length():
            raise Exception("TRAVERSE TOO LONG")

        ux, uy = self.slope()

        px = distance * ux + self.p1[0]
        py = distance * uy + self.p1[1]

        return (px, py)


    # check if the input point is on the line
    def check_on_line(self, point, debug=False):

        # check if p2 is the point ( do not check p1 to avoid rays )
        if not self.p2 is None:
            if round(point[0],5) == round(self.p2[0],5) and round(point[1],5) == round(self.p2[1],5):
                print("\tCHECK:",point, self.p1)
                print("\t",self)
                return True
        
        # build a temporary line from p1 to the input point
        # TODO this might not be the most efficient method
        temp = Line(self.p1, p2=point)
        if debug:
            print(str(round(self.angle%(2*np.pi),5)) + " - " + str(round(temp.angle%(2*np.pi),5)))
        # if the angle is not equivalent, return false
        if not round(self.angle%(2*np.pi),5) == round(temp.angle%(2*np.pi),5):
            return False

        # to be on the line, the point must be between the two existing points
        if self.length() >= temp.length():
            return True
        else:
            if debug:
                print(str(self.length()) + "<" + str(temp.length()))
            return False

    # find the intersection point with another line ~ None if there is none
    def intersection(self, line, debug=False, plot=False):
        
        # check if the angles are the same
        if (self.angle - line.angle) % 180 == 0:
            if debug: 
                print("LINES ARE PARALLEL")
            return None

        # find the intersection point
        point = self.__intersection_ray(line)

        # check if the point is on both lines
        if self.check_on_line(point, debug=debug) and line.check_on_line(point, debug=debug):
            if debug:
                print(point)
            return point
        else:
            if debug: 
                print("\tPOINT:", point)
                print("\tLINE ONE: " + str(self.check_on_line(point)) + "\t" + str(self))
                print("\tLINE TWO: " + str(line.check_on_line(point)) + "\t" + str(line))
            if plot:
                import matplotlib.pyplot as plt
                plt.plot(*self.plot())
                plt.scatter(point[0],point[1])
                plt.show()
                return point
            return None

    # find the intersection point of the two lines, treated as rays
    def __intersection_ray(self, line):

        dx, dy = self.slope()
        lx, ly = line.slope()

        V = (self.p1[1] - line.p1[1] + (dy/dx) * (line.p1[0] - self.p1[0])) / (ly - (dy/dx) * lx)

        px = line.p1[0] + lx * V
        py = line.p1[1] + ly * V

        return (px, py)


    def cross_product(self, line):

        ax = self.p2[0]-self.p1[0]
        ay = self.p2[1]-self.p1[1]

        bx = line.p2[0]-line.p1[0]
        by = line.p2[1]-line.p1[1]

        result = (ax * by) - (ay*bx)

        return result
    
    # return a zip of the line for plotting
    def plot(self):
        
        if not self.p2 is None:
            points = [self.p1, self.p2]
    
        else:
            dx, dy = self.slope()
            points = [self.p1, (dx*40+self.p1[0], dy*40+self.p1[1])]

        return zip(*points)


    def __eq__(self, line):
        return line.p1 == self.p1 and line.p2 == self.p2

    def __repr__(self):
        return str(self.p1) + " - " + str(self.p2) + " ANGLE: " + str(round(self.angle,2))
