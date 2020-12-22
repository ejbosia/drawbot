'''
Contour
This class has a list of Lines that make up the contour, and its heirarchy. the heirarchy determines if it is an inner or outer edge.

@author ejbosia
'''


import math

class Contour:

    def __init__(self, line_list, heirarchy):

        self.line_list = line_list
        self.heirarchy = heirarchy

        self.min, self.max = self.__bounds()

    # find the outer most coordinates of the Contour
    def __bounds(self):

        min_pt = list(self.line_list[0].p1)
        max_pt = list(self.line_list[0].p1)

        for line in self.line_list:
            
            if min_pt[0] < line.p1[0]:
                min_pt[0] = line.p1[0]

            if min_pt[1] < line.p1[1]:
                min_pt[1] = line.p1[1]

            if max_pt[0] > line.p1[0]:
                max_pt[0] = line.p1[0]

            if max_pt[1] > line.p1[1]:
                max_pt[1] = line.p1[1]

        return tuple(min_pt), tuple(max_pt)


    # find all intersections with the line
    def intersection(self, line):
        
        points = []

        for l in self.line_list:
            temp = line.intersection(l)

            if temp is None:
                continue
            else:
                points.append(temp)

        return points

    def __repr__(self):
        output = str(self.heirarchy) + " - "
        for line in self.line_list:
            output += str(line.p1) + ","

        output += str(self.line_list[-1])
        return output
