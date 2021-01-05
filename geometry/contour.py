'''
Contour
This class has a list of Lines that make up the contour, and its heirarchy. the heirarchy determines if it is an inner or outer edge.

@author ejbosia
'''
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


import math
from geometry.line import Line
from geometry.point import Point


class Contour:

    def __init__(self, line_list, heirarchy):

        self.line_list = line_list
        self.heirarchy = heirarchy

        self.intersection_list = []
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


    # find the maximum corner point of the contour
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


    # find all intersections with the line
    def intersection(self, line):
        
        points = []

        for l in self.line_list:
            temp = l.intersection(line)      
            if temp is None:
                continue
            else:
                points.append(temp)

        return points

    # save the intersection points to a dictionary by row-number
    def save_intersection(self, line, line_number):
        
        # get the intersections
        intersections = self.intersection(line)

        # if there are intersections, add to the list
        if intersections:
            if not line_number in self.intersection_points:
                self.intersection_points[line_number] = []
            
            for pt in intersections:
                self.intersection_points[line_number].append(Point(pt[0],pt[1], self))
            return True
        else:
            return False


    # save the ordered list of intersection points
    def save_intersection_list(self):

        for line in self.line_list:

            temp_distance = []
            temp_points = []

            for key in self.intersection_points:

                for point in self.intersection_points[key]:

                    temp_point = point.tuple()
                    
                    if line.check_on_line(temp_point):
                        distance = math.sqrt((line.p1[0] - point.x)**2 + (line.p1[1] - point.y)**2)
                        temp_distance.append(distance)
                        temp_points.append(point)

            self.intersection_list.extend([x for _,x in sorted(zip(temp_distance,temp_points))])


    # find the line that contains the point
    def find_point(self, point):

        # loop through each line, and check if the point is on the line
        for line in self.line_list:
            if line.check_on_line(point):
                return line

        return None


    # check if the point is on the contour
    def check_on_contour(self, point):

        for line in self.line_list:
            if line.check_on_line(point):
                return True
        
        return False


    # check if the point is on the corner of the line
    def check_peak(self, point, int_line):

        p1 = None
        p2 = None

        for line in self.line_list:
            if line.p1 == point:
                p1 = line.p2  
            if line.p2 == point:    
                p2 = line.p1
            
        if p1 is None or p2 is None:
            return False

        # check the positions of the lines
        line1 = Line(line.p1, p2 = p1)
        line2 = Line(line.p1, p2 = p1)

        cross_one = int_line.cross_product(line1) > 0
        cross_two = int_line.cross_product(line2) > 0

        if cross_one == cross_two:
            return True
        else:
            return False


    # return X and Y lists to plot
    def plot(self):

        # create the lists of points
        X = [self.line_list[0].p1[0]]
        Y = [self.line_list[0].p1[1]]

        for line in self.line_list:
            X.append(line.p2[0])
            Y.append(line.p2[1])

        return X,Y


    # return a hash of the contour to all dictionary
    def __hash__(self):
        return hash(str(self.heirarchy))


    # return a string representation of the contour
    def __repr__(self):
        output = str(self.heirarchy) + " - "
        for line in self.line_list:
            output += str(line.p1) + ","

        output += str(self.line_list[-1].p2)
        return output
