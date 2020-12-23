'''
Contour
This class has a list of Lines that make up the contour, and its heirarchy. the heirarchy determines if it is an inner or outer edge.

@author ejbosia
'''
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


import math
from geometry.line import Line



class Contour:

    def __init__(self, line_list, heirarchy):

        self.line_list = line_list
        self.heirarchy = heirarchy

        self.intersection_points = {}

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

    # return true if this contour is a parent contour
    def is_parent(self):
        return self.heirarchy[3] == -1


    # rotate a point
    def rotate_point(self, point, angle):
        # calculate the relative distance in the direction
        # --> rotate the point so the "x" value is in the direction
        # --> we want to rotate the point "back" to 0, so we use -angle
        s = math.sin(angle)
        c = math.cos(angle)

        x = point[0] * c - point[1] * s
        y = point[0] * s + point[1] * c

        return (x,y)


    def find_maximum_point(self, angle):

        maximum = self.rotate_point(self.line_list[0].p1, -angle)[0]
        maximum_point = self.line_list[0].p1

        # loop through each point
        for line in self.line_list:
            
            new_point = self.rotate_point(line.p1, -angle)

            if maximum < new_point[0]:
                maximum = new_point[0]
                maximum_point = line.p1

        return maximum_point


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
    def intersection(self, line, debug=False, plot=False):
        
        points = []

        for l in self.line_list:
            temp = l.intersection(line, debug=debug, plot=plot)      
            if temp is None:
                continue
            else:
                points.append(temp)


        if debug:
            print(points)

        return points

    # save the intersection points to a dictionary by row-number
    def save_intersection(self, line, line_number):
        
        # get the intersections
        intersections = self.intersection(line)

        # if there are intersections, add to the list
        if intersections:
            if not line_number in self.intersection_points:
                self.intersection_points[line_number] = []
            
            self.intersection_points[line_number].extend(intersections)
            return True
        else:
            return False




    # find the line that contains the point
    def __find_point(self, point):

        # loop through each line, and check if the point is on the line
        for line in self.line_list:
            if line.check_on_line(point):
                return line

        return None


    def check_on_contour(self, point):

        for line in self.line_list:
            if line.check_on_line(point):
                return True
        
        return False

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

    # return X and Y lists to plot
    def plot(self):

        # create the lists of points
        X = [self.line_list[0].p1[0]]
        Y = [self.line_list[0].p1[1]]

        for line in self.line_list:
            X.append(line.p2[0])
            Y.append(line.p2[1])

        return X,Y

    # return a string representation of the contour
    def __repr__(self):
        output = str(self.heirarchy) + " - "
        for line in self.line_list:
            output += str(line.p1) + ","

        output += str(self.line_list[-1].p2)
        return output
