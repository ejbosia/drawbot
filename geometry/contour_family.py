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
    def generate_intersection_points(self, line_thickness, angle):

        current_point = self.__starting_point(angle)

        # generate inifinite lines starting from the starting point + line_thickness perpendicular to the angle
        # the infinite lines comprise of two rays with directions of angle and angle + pi
        # once a "no intersection" point is reached (for both rays), the process stops

        # start the loop
        intersections = True

        perpendicular_angle = angle + (np.pi/2)

        line_number = 0        

        # loop until there are no intersections
        # while intersections:
        for _ in range(34):
            
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

        print(self.parent_contour.intersection(ray1, debug=True))


        plt.plot(*ray1.plot())
        plt.plot(*ray2.plot())

        X,Y = self.parent_contour.plot()
        plt.plot(X,Y)

        for key in self.parent_contour.intersection_points.keys():
            for point in self.parent_contour.intersection_points[key]:
                plt.scatter(point.x, point.y)

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

    # return all of the points at the row, grouped by contour
    def __get_contour_rowpoints(self, row):

        points = {self.parent_contour:self.parent_contour.intersection_points[row]}
        
        for child_contour in self.children:
            
            if row in child_contour.intersection_points:
                points[child_contour] = child_contour.intersection_points[row]

        return points


    def __get_closest_point(self, point, points_dict):

        temp = dict(points_dict)

        # find the point in the dict
        for key in temp:
            print("GET CLOSEST:", point, "\t", temp[key], "\t", key == self.parent_contour)
           
            if point in temp[key] and key == self.parent_contour:
                index = temp[key].index(point)

                if index%2 == 0:
                    temp[key] = temp[key][index+1:]
                else:
                    temp[key] = temp[key][0:index]

                break

            elif point in temp[key]:

                index = temp[key].index(point)

                if index%2 == 1:
                    temp[key] = temp[key][index+1:]
                else:
                    temp[key] = temp[key][0:index]
                break

        # find the closest point in temp

        # set the closest point to start at the first point

        first = True
        closest_point = None
        contour = None

        print("\tTEMP:", list(temp.values()))

        for key in temp:
            for new_point in temp[key]:
                
                if first and not new_point.visited:
                    first = False
                    closest_point = new_point
                    minimum = point.distance(new_point)
                    contour = key

                elif not new_point.visited:
                    new_distance = point.distance(new_point)

                    if minimum > new_distance:
                        closest_point = new_point
                        minimum = new_distance
                        contour = key

        print("\tCLOSEST:", closest_point)


        return closest_point, contour


    def __next_contour_point(self, previous_point, contour, row):

        print("NEXT:", row)

        if not row in contour.intersection_points:
            return None
        
        temp_point = (previous_point.x,previous_point.y)

        # get the line the point is on
        line = contour.find_point(temp_point)


        index = contour.line_list.index(line)

        lines = []

        possible_points = contour.intersection_points[row]

        if possible_points:
            minimum = previous_point.distance(possible_points[0])
            closest_point = possible_points[0]

            for point in possible_points:
                
                new_distance = previous_point.distance(point)

                if minimum > new_distance:
                    minimum = new_distance
                    closest_point = point

            if not closest_point.visited:
                return closest_point

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

            # get all the points
            points_dict = self.__get_contour_rowpoints(row)

            # find closest point that is not part of the current contour (except parent)
            next_point, next_contour = self.__get_closest_point(point, points_dict)
            
            if next_point is None:
                break

            path.append(next_point)
            next_point.set_visited()

            # traverse contour (increase row number)
            row += 1

            # find the next point (none if none)
            point = self.__next_contour_point(next_point, next_contour, row)

        
        return path


    def generate_total_path(self, line_thickness, angle):


        point = []

        path = []
        total_path = []

        self.generate_intersection_points(line_thickness, angle)

        print(self.parent_contour.intersection_points)

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
        
