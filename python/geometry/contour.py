'''
Contour
This class has a list of Lines that make up the contour, and its heirarchy. the heirarchy determines if it is an inner or outer edge.

@author ejbosia
'''
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


import math
import numpy as np

from geometry.line import Line
from geometry.point import Point


class Contour:

    def __init__(self, vertex_list):

        self.vertex_list = vertex_list

    # rotate all points in contour
    def rotate(self, angle):
        
        for i, _ in enumerate(self.vertex_list):
            self.vertex_list[i].rotate(angle)

    # add up all of the angles in the contour and divide by the number of vertices
    def total_angle(self):
        prev_list = self.vertex_list[-1:] + self.vertex_list[0:-1]   # previous point
        next_list = self.vertex_list[1:] + self.vertex_list[0:1]     # next point
        
        total_angle = 0

        for p0, p1, p2 in zip(prev_list, self.vertex_list, next_list):
            a = p1.angle(p2)
            a2 = p1.angle(p0)
    
            total_angle += (a-a2)%(2*np.pi)

        return total_angle / len(self.vertex_list)


    # find all intersections with the line
    def intersection(self, line):
        
        points = []

        next_p = self.vertex_list[1:] + self.vertex_list[0:1]

        for i, p in enumerate(self.vertex_list):

            temp = line.intersection(Line(p,next_p[i]))      

            if temp is None:
                continue
            else:
                points.append(temp)

        return points


    # move points towards the center
    def dis_trans(self, dis=1):
        
        # loop through each point, move point inwards
        # this requires the previous and the next point
        
        prev_list = self.vertex_list[-1:] + self.vertex_list[0:-1]   # previous point
        next_list = self.vertex_list[1:] + self.vertex_list[0:1]     # next point
        
        new_list = []

        for p, prev_p, next_p in zip(self.vertex_list,prev_list, next_list ):
            
            a = p.angle(next_p)
            a2 = p.angle(prev_p)

            # if a == a2:
            #     print(p)
                    
            a3 = (a-a2)%(2*np.pi)

            a3 /= 2
            
            r = dis/np.sin(a3)

            a3 += a2

            temp = Point(p.x, p.y)
            temp.translate_DA(r, a3)

            new_list.append(temp)
        
        return Contour(new_list)

    # try to find and remove areas of the contour with overlapping lines
    def simplify(self):
        
        new_list = []
        prev_list = self.vertex_list[-1:] + self.vertex_list[0:-1]   # previous point
        next_list = self.vertex_list[1:] + self.vertex_list[0:1]     # next point

        # loop through the vertex list and remove duplicates
        for p0, p1, p2 in zip(prev_list, self.vertex_list, next_list):

            if p1 == p2:
                continue
            # if the angle around p1 is 180, remove p1
            elif(((p1.angle(p0)-np.pi)%np.pi) == (p1.angle(p2)%np.pi)):
                continue
            else:
                new_list.append(p1)

        self.vertex_list = new_list

        self._simplify_angles()

    # try to find and remove areas of the contour with overlapping lines
    def _simplify_angles(self):
        
        new_list = []
        prev_list = self.vertex_list[-1:] + self.vertex_list[0:-1]   # previous point
        next_list = self.vertex_list[1:] + self.vertex_list[0:1]     # next point

        # loop through the vertex list and remove duplicates
        for p0, p1, p2 in zip(prev_list, self.vertex_list, next_list):

            # if the angle around p1 is 180, remove p1
            if(((p1.angle(p0)-np.pi)%np.pi) == (p1.angle(p2)%np.pi)):
                continue
            else:
                new_list.append(p1)

        self.vertex_list = new_list


    # break the contour into smaller pieces if there are self intersections
    def self_intersections(self):
        
        next_list = self.vertex_list[1:] + self.vertex_list[0:1]     # next point

        new_list = [[]]

        intersection_list = []

        current_contour = 0

        # find the self intersections
        for p1, p2 in zip(self.vertex_list, next_list):
            
            line = Line(p1, p2)

            intersections = self.intersection(line)
            
            new_list[current_contour].append(p1)
            

            # if intersections:
            #     print(intersections, intersection_list, intersections[0] in intersection_list)

            # if the intersection point exists, move to the previous contour
            if intersections and intersections[0] in intersection_list:

                current_contour -= 1
            
            # if the intersection point does not exist, create a new contour and save the point in each
            elif intersections:
                
                intersection_list.extend(intersections)

                new_list[current_contour].append(intersections[0])

                current_contour += 1
                new_list.append([intersections[0]])

        # return a list of all new contours
        return [Contour(x) for x in new_list]
            



    # return X and Y lists to plot
    def plot(self):

        # create the lists of points
        X = []
        Y = []

        for vertex in self.vertex_list:
            X.append(vertex.x)
            Y.append(vertex.y)

        return X,Y


    # return a string representation of the contour
    def __repr__(self):
        output = ""
        for vertex in self.vertex_list:
            output += str(vertex) + ","

        return output
