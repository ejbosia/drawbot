'''
Point
A point has an X and Y coordinate, and a boolean value for if it has been visited

@author ejbosia
'''

import math
import numpy as np

class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y


    def distance(self, other):
        return math.sqrt((self.x-other.x)**2 + (self.y-other.y)**2)


    def translate_XY(self, dx, dy):
        self.x += dx
        self.y += dy


    def translate_DA(self, dis, a):

        dx = dis * np.cos(a)
        dy = dis * np.sin(a)

        self.translate_XY(dx, dy)


    def rotate(self, angle):
        s = math.sin(angle)
        c = math.cos(angle)

        x = self.x * c - self.y * s
        y = self.x * s + self.y * c

        self.x = x
        self.y = y



    def angle(self, other):
        
        dx = other.x-self.x
        dy = other.y-self.y

        return np.arctan2(dy,dx) % (2*np.pi)


    
    def tuple(self):
        return (self.x,self.y)

    def __lt__(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        
        return (dy + dx) > 0

    def __le__(self, other):
        return self < other or self == other
    
    def __eq__(self, other):
        return round(self.x,10) == round(other.x,10) and round(self.y,10) == round(other.y,10)
    
    def __ne__(self, other):
        return not self == other
    
    def __gt__(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        
        return (dy + dx) < 0
    
    def __ge__(self, other):
        return self > other or self == other

    def __hash__(self):
        return hash(str(self.x)+str(self.y))

    def __repr__(self):
        return "(" + str(round(self.x,2)) + "," + str(round(self.y,2)) + ")"

    