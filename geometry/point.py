'''
Point
A point has an X and Y coordinate, and a boolean value for if it has been visited

@author ejbosia
'''

import math

class Point:

    def __init__(self, x, y, c):
        self.x = x
        self.y = y
        self.c = c
        self.visited = False


    def set_visited(self):
        self.visited = True


    def distance(self, other):
        return math.sqrt((self.x-other.x)**2 + (self.y-other.y)**2)


    def __lt__(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        
        return (dy + dx) > 0

    def __le__(self, other):
        return self < other or self == other
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __ne__(self, other):
        return not self == other
    
    def __gt__(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        
        return (dy + dx) < 0
    
    def __ge__(self, other):
        return self > other or self == other


    def __repr__(self):
        return "(" + str(round(self.x,2)) + "," + str(round(self.y,2)) + ")" # + ")\t" + str(self.visited)

    