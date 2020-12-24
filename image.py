import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import interactive
import datetime
import gcode as GC
import pandas as pd
import math

import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

from geometry.line import Line
from geometry.contour import Contour
from geometry.contour_family import Family


def ravel_lines(line_list):

    X = []
    Y = []

    for line in line_list:
        if not X and not Y:
            X.append(line.p1[0])
            Y.append(line.p1[1])

        X.append(line.p2[0])
        Y.append(line.p2[1])
    
    return X, Y

def plot_contours(contour_list, show=True, points=True):

    for contour in contour_list:

        X,Y = ravel_lines(contour.line_list)
        plt.plot(X,Y)

        if points:
            for x,y in zip(X,Y):
                plt.scatter(x,y)
    
    if show:
        plt.show()


# create border lines for the image
# return a list of lists of lines
def generate_border_lines(image):

    contours,heirarchy = cv2.findContours(image, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)  

    contour_list = []

    for contour,heirarchy in zip(contours, heirarchy[0]):
        line_list = []
        pt0 = None
        for c in contour:
            # if this is the first point do not create a line
            if not pt0 is None:
                line_list.append(Line(pt0, p2=tuple(c[0])))
            
            pt0 = tuple(c[0])

        # add the last line from the last first point to the starting point
        line_list.append(Line(pt0, p2 = tuple(contour[0][0])))

        contour_list.append(Contour(line_list, heirarchy))

    return contour_list


# get all of the children of the parent contour
def get_children(contour_list, parent_contour):

    child_list = []

    first_child_index = parent_contour.heirarchy[2]
    child = contour_list[first_child_index]
    child_list.append(child)


    # loop while there are more children
    while not child.heirarchy[0] == -1:
        next_child_index = child.heirarchy[0]
        child = contour_list[next_child_index]
        child_list.append(child)
    
    # return the list of children
    return child_list

def create_contour_families(contour_list):

    family_list = []

    # find the first parent contour
    for contour in contour_list:
        
        # start with a parent contour
        if contour.is_parent():

            # if there are no children, create an empty family with only the parent contour
            if contour.heirarchy[2] == -1:
                child_list = []
            # otherwise, find all of the children
            else:
                child_list = get_children(contour_list, contour)

            family_list.append(Family(contour, child_list))

    return family_list



# fill contours towards other edge
# hole contours away from other edge
def fill_direction(contour, point, angle):

    # force the angle within 0-2PI
    angle = angle % (2*np.pi)

    # find the direction that is "inside" the contour
    ray = Line(point, angle = angle)
    
    # if number of intersections is even, the direction must be the opposite for "fill" contours
    if (len(contour.intersection(ray))%2==0) and contour.heirarchy[3] == -1:
        angle = angle - math.pi
    # if number of intersections is odd, the direction must be the opposite for "hole" contours
    elif (len(contour.intersection(ray))%2==1) and not (contour.heirarchy[3] == -1):
        angle = angle - math.pi
    return angle



# find the closest intersection from the ray - returns the contour and the point
def find_closest_intersection(contour_list, ray):

    '''
    # THIS DOES NOT SEEM TO WORK - CAN REVISIT WHEN PERFORMANCE IS AN ISSUE
    possible_contours = []

    # find all contours that intersect (fast)
    for contour in contour_list:
        if contour.fast_intersection(ray):
            possible_contours.append(contour)
    '''
    possible_contours = contour_list

    points = []
    contours = []

    # find all intersection points
    for contour in possible_contours:
        point = contour.intersection(ray)
        if not point is None:
            points.extend(point)

            # add a contour for each point
            for _ in range(len(point)):
                contours.append(contour)

    # find the closest point
    length = Line(ray.p1, p2 = points[0]).length()

    closest_point = points[0]
    closest_contour = contours[0]

    for contour, point in zip(contours,points):
        new_length = Line(ray.p1, p2 = point).length()
        if length > new_length:
            length = new_length
            closest_point = point
            closest_contour = contour

    return closest_contour, closest_point



# create a single path
def create_path(contour_list, line_thickness, angle, start_contour, start_point):

    temp_point = start_point
    contour = start_contour

    line_x = [start_point[0]]
    line_y = [start_point[1]]

    perpendicular_angle = angle + (np.pi/2)
    
    while(True):
    
        if contour.heirarchy[3] == -1:        
            temp_ray = Line(temp_point, angle=angle)
            intersections = contour.intersection(temp_ray, debug=False)

            # if contour.check_on_contour(temp_point):
            #     intersections = [temp_point]

            if not intersections:
                temp_ray = Line(temp_point, angle=angle-math.pi)
                intersections = contour.intersection(temp_ray)
        
        else:
            angle = (angle+np.pi)%(2*np.pi)
        
            temp_ray = Line(temp_point, angle=angle)
            intersections = contour.intersection(temp_ray, debug=False, plot=False)
            
            # if contour.check_on_contour(temp_point):
            #     intersections = [temp_point]
            if not intersections:
                temp_ray = Line(temp_point, angle=angle-math.pi)
                intersections = contour.intersection(temp_ray)

        # if there are no intersections, break the loop
        if not intersections:
            break

        min_length = Line(temp_ray.p1, p2=intersections[0]).length()

        # find the closest intersection point
        for i in intersections:
            new_length = Line(temp_ray.p1, p2=i).length()
            if new_length <= min_length:
                new_point = i
                min_length = new_length

        
        line_x.append(new_point[0])
        line_y.append(new_point[1])


        # determine a direction
        angle = fill_direction(contour, new_point, angle)

        ray = Line(new_point, angle=angle)

        contour, point = find_closest_intersection(contour_list, ray)

        ray.p2 = point

        line_x.append(point[0])
        line_y.append(point[1])

        plot_contours(contour_list,show=False,points=False)
        
        plt.plot(line_x, line_y)

        dx = np.cos(perpendicular_angle)
        dy = np.sin(perpendicular_angle)

        temp_point = (dx*line_thickness+ray.p2[0], dy*line_thickness+ray.p2[1])

    plt.show()


    print("RETURN SOMETHING??")



def fill_contours(contour_list, line_thickness=1, angle=math.pi/3):

    start_point = contour_list[1].find_maximum_point(angle-(np.pi/2))
    plt.scatter(start_point[0],start_point[1])

    traverse_amount = -line_thickness

    perpendicular_angle = angle + (np.pi/2)

    dx = np.cos(perpendicular_angle)
    dy = np.sin(perpendicular_angle)

    start_point = (dx*line_thickness+start_point[0], dy*line_thickness+start_point[1])

    create_path(contour_list, line_thickness, angle, contour_list[1], start_point)




def find_available_point(rows):

    for row in rows:

        for point in rows:

            if not point.visited:
                return point

    return None


def generate_path(rows):

    # pick a starting point
    point = find_available_point(rows)

    path = []

    d = 1

    while not point is None:
        
        done = False
        index = [(i, row.index(point)) for i, row in enumerate(rows) if point in row][0]

        # move through the list
        while not done:
            
            # add the current point
            path.append(point)
            row[index[0]][index[1]].set_visited()

            # move to the next point
            index[1] += d

            point = row[index[0]][index[1]]

            # move to the next row
            index[0] += 1

            # check if the next row has the index
            point = row[index[0]][index[1]]

        




def main(file="picture.png", inverse=False, resize = 8):
    print(file)

    image = cv2.imread(file, 0)

    image = cv2.resize(image, None, fx=resize, fy=resize, interpolation=cv2.INTER_NEAREST)

    if inverse:
        image = 255-image

    # create contours
    contours = generate_border_lines(image)

    # organize contours into families of contours
    family_list = create_contour_families(contours)

    # plot each family
    # for family in family_list:
    #     family.plot(show=True)

    line_thickness = 12
    angle = np.pi/6

    
    total_path = []

    total_start = datetime.datetime.now()

    #
    for index, family in enumerate(family_list):
        start = datetime.datetime.now()
        total_path.append(family.generate_total_path(line_thickness, angle))
        print("FAMILY:",index,"\t",datetime.datetime.now() - start)
    # for i in range(14):
    # total_path.append(family_list[1].generate_total_path(line_thickness, angle))
    # print(datetime.datetime.now() - total_start)

    X = []
    Y = []


    for family_path in total_path:



        for path in family_path:

            X.append([])
            Y.append([])
            for point in path:
                X[-1].append(point.x)
                Y[-1].append(point.y)
    
    family_list[1].plot()
    
    for x,y in zip(X,Y):
        plt.plot(x,y)

    plt.show()
    # fill_contours(contours)

if __name__ == "__main__":
    main()
