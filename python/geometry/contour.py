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

        if self.vertex_list:
            self.min_point = self._min_xy_bound()


    def _min_xy_bound(self):

        x = self.vertex_list[0].x
        y = self.vertex_list[0].y     

        for p in self.vertex_list:

            if p.x < x:
                x = p.x
            if p.y < y:
                y = p.y
        
        return Point(x,y)



    # rotate all points in contour
    def rotate(self, angle):
        
        for i, _ in enumerate(self.vertex_list):
            self.vertex_list[i].rotate(angle)

    # get the centroid of the contour
    def centroid(self):

        x = 0
        y = 0

        for p in self.vertex_list:
            x += p.x
            y += p.y

        x /= len(self.vertex_list)
        y /= len(self.vertex_list)

        return Point(x,y)


    # check if the point is in the contour
    # we can use an outside ray to the point to check the number of intersections
    def contains(self, point):

        test_point = self.min_point.copy()

        test_point.translate_XY(-1,-1)

        # -1 -1 should be outside the contour
        line = Line(test_point, point)

        next_list = self.vertex_list[1:] + self.vertex_list[0:1]     # next point

        n = 0

        for p1, p2 in zip(self.vertex_list, next_list):

            temp = Line(p1,p2)

            if line.fast_check_intersection(temp):
                n += 1
                
            # if the line intersects at the point, add one
            if line.fast_on_line(p1):
                n -= 1


        

        return n % 2 == 1



    # check if all of the points in a contour are within the contour
    def contains_contour(self, contour):
        for p in contour.vertex_list:
            if not self.contains(p):
                return False

        return True



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

    # return true if point is within a distance from the contour
    def vertex_close(self, point, distance):

        next_list = self.vertex_list[1:] + self.vertex_list[0:1]

        for p1, p2 in zip(self.vertex_list, next_list):

            if Line(p1,p2).distance(point) < distance:
                return True

        return False

    def contour_close(self, contour, distance):
        
        for p in contour.vertex_list:
            if self.vertex_close(p, distance):
                return True

        return False

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
                    
            a3 = (a-a2)%(2*np.pi)

            a3 /= 2
            
            r = dis/np.sin(a3)

            a3 += a2

            temp = Point(p.x, p.y)
            temp.translate_DA(r, a3)

            new_list.append(temp)
        
        return Contour(new_list)


    # return true if point is within a distance from the contour
    def self_vertex_close(self, point, distance):

        next_list = self.vertex_list[1:] + self.vertex_list[0:1]

        for p1, p2 in zip(self.vertex_list, next_list):

            dis = Line(p1,p2).distance_2(point)
            if dis == 0:
                continue
            if dis < distance:
                print("DIS",dis, point, "\tLINE:", p1,p2)
                return True

        return False

    def self_contour_close(self, contour, distance):
        
        for p in contour.vertex_list:
            if self.self_vertex_close(p, distance):
                return True

        return False

    # try to find and remove areas of the contour with overlapping lines
    def simplify(self, distance):
        
        new_list = []
        next_list = self.vertex_list[1:] + self.vertex_list[0:1]     # next point

        # loop through the vertex list and remove duplicates
        for p1, p2 in zip(self.vertex_list, next_list):

            if p1.distance(p2) < distance:
                continue
            else:
                new_list.append(p1)


        if len(new_list) > 2:
            self.vertex_list = new_list
        else:
            self.vertex_list = []

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

        print("START:",self.vertex_list[0])

        # find the self intersections
        for p1, p2 in zip(self.vertex_list, next_list):
            
            line = Line(p1, p2)

            intersections = self.intersection(line)
            
            new_list[current_contour].append(p1)
            
            sort_intersections = []

        
            # sort intersections
            for i in intersections:

                if not sort_intersections:
                    sort_intersections.append(i)

                else:

                    dis  = p1.distance(i)
                    # find the index and insert between
                    for j, s in enumerate(sort_intersections):
                        index = j    
                        if p1.distance(s) < dis:
                            break
                    
                    # insert the index into the array
                    sort_intersections = sort_intersections[0:index] + [i] + sort_intersections[index:]

            for i in sort_intersections:
                # if the intersection point exists, move to the previous contour
                if i in intersection_list:

                    current_contour -= 1
                
                # if the intersection point does not exist, create a new contour and save the point in each
                else:
                    
                    intersection_list.append(i)

                    new_list[current_contour].append(i)

                    current_contour += 1
                    new_list.append([i])

        print(intersection_list)
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
        output = "CONTOUR: "
        for vertex in self.vertex_list:
            output += str(vertex) + ","

        return output
