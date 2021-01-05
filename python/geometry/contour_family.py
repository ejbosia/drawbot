'''
Family
This holds a parent contour and its children.

@author ejbosia
'''

import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


import math
import numpy as np
import matplotlib.pyplot as plt
import datetime

from geometry.line import Line
from geometry.contour import Contour
from geometry.point import Point


class Family:

    def __init__(self, parent_contour, children=[]):
        self.parent_contour = parent_contour
        self.children = children

    # get the starting point to process the family
    def __starting_point(self, angle):
        return self.parent_contour.find_maximum_point(angle-(np.pi/2))

    # get all of the intersections of a line on the family ~ save to the contours
    def intersection(self, line, line_number):

        if not self.parent_contour.save_intersection(line,line_number):
            return False

        for child_contour in self.children:
            child_contour.save_intersection(line,line_number)

        return True

    # generate the intersection points on each contour in the family
    def generate_intersection_points(self, line_thickness, angle, time=True):

        if time:
            start = datetime.datetime.now()


        current_point = self.__starting_point(angle)

        # generate inifinite lines starting from the starting point + line_thickness perpendicular to the angle
        # the infinite lines comprise of two rays with directions of angle and angle + pi
        # once a "no intersection" point is reached (for both rays), the process stops

        # start the loop
        intersections = True

        perpendicular_angle = angle + (np.pi/2)

        line_number = 0        

        # loop until there are no intersections
        while intersections:
            
            points = []

            # generate a new line
            dx = np.cos(perpendicular_angle)
            dy = np.sin(perpendicular_angle)

            current_point = (dx*line_thickness+current_point[0], dy*line_thickness+current_point[1])

            ray1 = Line(current_point, angle=angle)
            ray2 = Line(current_point, angle=angle-np.pi)

            # check the line for intersections against the parent and all children
            direction_one = self.intersection(ray1, line_number) 
            direction_two = self.intersection(ray2, line_number)

            intersections = direction_one or direction_two
            
            line_number += 1

        self.parent_contour.save_intersection_list()
        
        for child in self.children:
            child.save_intersection_list()
        
        if time:
            logging.info("GENERATE POINTS: " + str(datetime.datetime.now()-start))

        # self.plot_intersection_list()


    def plot_intersection_list(self):
        X = []
        Y = []

        for p in self.parent_contour.intersection_list:
            X.append(p.x)
            Y.append(p.y)

        for line in self.parent_contour.line_list:
            plt.scatter(line.p1[0], line.p1[1])

        X,Y = self.parent_contour.plot()
        plt.plot(X,Y)

        plt.show()
        

    # find available point (and row location)
    def __find_available_point(self):
        
        # will want to improve performance here

        # check parent contour

        contour = self.parent_contour

        for key in contour.intersection_points:
            for point in contour.intersection_points[key]:
                if point.visited == False:
                    return point, key

        # check each child

        for contour in self.children:
            for key in contour.intersection_points:
                for point in contour.intersection_points[key]:
                    if point.visited == False:
                        return point, key

        return None,None


    # get all of the intersection points in the row
    def __get_contour_rowpoints(self, row):

        if not row in self.parent_contour.intersection_points:
            return None

        points = {}

        for point in self.parent_contour.intersection_points[row]:
            points[point] = self.parent_contour
        
        for child_contour in self.children:
            if row in child_contour.intersection_points:
                for point in child_contour.intersection_points[row]:
                    points[point] = child_contour
        return points


    # remove peaks as possible intersections
    def __remove_peaks(self,row_points, points_dict):

        if len(row_points)%2==1:

            start = (row_points[0].x, row_points[0].y)
            end = (row_points[-1].x, row_points[-1].y)
            intersection_line = Line(start, p2 = end)

            for p in row_points:
                c = points_dict[p]

                # remove the peak
                if(c.check_peak((round(p.x,5),round(p.y,5)), intersection_line)):
                    row_points.remove(p)

        return row_points


    # get the closest point in the correct direction
    def __get_closest_point(self, point, points_dict):

        row_points = list(points_dict.keys())

        row_points.sort()

        row_points = self.__remove_peaks(row_points, points_dict)

        try:
            index = row_points.index(point)
        except:
            return None, None

        if(len(row_points) < 2):
            row_points[index].set_visited()
            return None, None

        if index % 2 == 0:
            closest_point = row_points[(index+1)%len(row_points)]

        elif index % 2 == 1:
            closest_point = row_points[index-1]
            
        contour = points_dict[closest_point]

        if closest_point.visited:
            return None, None

        return closest_point, contour



    # return the next contour point
    def __next_contour_point(self, point, contour, row):

        if not row in contour.intersection_points:
            return None

        row_points = contour.intersection_points[row]

        index = contour.intersection_list.index(point)

        # get the next two possible points
        test_one = contour.intersection_list[(index+1)%(len(contour.intersection_list))]
        test_two = contour.intersection_list[index-1]

        if test_one in row_points:
            return test_one

        elif test_two in row_points:
            return test_two

        else:
            return None
  

    # create a path to fill the contour
    def generate_path(self, line_thickness, angle):
        
        point, row = self.__find_available_point()
        next_point = point

        if point is None:
            return None

        path = []

        while not point is None:

            path.append(point)
            point.set_visited()

            points_dict = self.__get_contour_rowpoints(row)

            # next_point, next_contour = self.__get_closest_point(point, points_dict)
            next_point, next_contour = self.__get_closest_point(point, points_dict)

            if next_point is None:
                break

            path.append(next_point)
            next_point.set_visited()

            # traverse contour (increase row number)
            row += 1

            point = self.__next_contour_point(next_point, next_contour, row)

        return path


    def generate_total_path(self, line_thickness, angle):

        point = []

        path = []
        total_path = []

        self.generate_intersection_points(line_thickness, angle)

        while not path is None:

            path = self.generate_path(line_thickness, angle)

            if not path is None:
                total_path.append(path)

        return total_path

        
    # plot the family  
    def plot(self, show=False):

        X,Y = self.parent_contour.plot()

        plt.plot(X,Y)
        
        for child_contour in self.children:
            
            X,Y = child_contour.plot()
            plt.plot(X,Y)
        
        if show:
            plt.show()
        
