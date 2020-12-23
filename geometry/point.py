'''
Point
A point has an X and Y coordinate, and a boolean value for if it has been visited

@author ejbosia
'''


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = False


    def set_visited(self):
        self.visited = True

    