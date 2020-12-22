'''
Contour
This class has a list of Lines that make up the contour, and its heirarchy. the heirarchy determines if it is an inner or outer edge.

@author ejbosia
'''


import math
from geometry.line import Line

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

    # return true if there could be an intersection with an input ray
    def fast_intersection(self, ray):

        # create lines to the four corners of the bounding rectangle
        l1 = Line(ray.p1, p2 = (self.min[0], self.min[1]))
        l2 = Line(ray.p1, p2 = (self.max[0], self.min[1]))
        l3 = Line(ray.p1, p2 = (self.min[0], self.max[1]))
        l4 = Line(ray.p1, p2 = (self.max[0], self.max[1]))

        lines = [l2,l3,l4]

        # check if the angles are above or below the ray
        # if all are above or below, there is no intersection

        start = l1.angle > ray.angle

        for l in lines:
            
            # if the start and current angle are on opposite sides of the ray, return true
            if start == (l.angle < ray.angle):
                return True
        
        return False


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


    # find the line that contains the point
    def __find_point(self, point):

        # loop through each line, and check if the point is on the line
        for line in self.line_list:
            if line.check_on_line(point):
                return line

        return None


    # rotate the lines so the starting line is the first in the list
    def __rotate_lines(self, start_line):

        # loop to the input line
        for index, line in enumerate(self.line_list):
            if start_line == line:
                
                # move the end of the list to the start
                new_list = self.line_list[index:]

                # extend the start of the list (before found line) to the end
                end = self.line_list[0:index]
                new_list.extend(end)

                return new_list


    # find a point that is around the contour
    def traverse(self, point, distance):
        
        # find the starting point in the contour
        start_line = self.__find_point(point)

        # move across the lines by length
        new_list = self.__rotate_lines(start_line)

        # loop through the lines in the new list
        for line in new_list:
            if distance > line.length():
                distance = distance - line.length()
            else:
                return line.traverse(distance)

        return None


    # return a string representation of the contour
    def __repr__(self):
        output = str(self.heirarchy) + " - "
        for line in self.line_list:
            output += str(line.p1) + ","

        output += str(self.line_list[-1].p2)
        return output
