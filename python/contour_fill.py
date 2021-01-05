'''
Contour Fill
This file contains the logic for creating a contour fill of a black and white image

@author ejbosia
'''

import cv2
import numpy as np
import matplotlib.pyplot as plt
import datetime
import math

import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

import gcode as GC
from geometry.line import Line
from geometry.contour import Contour
from geometry.contour_family import Family


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


# combine contours into single level parent-children relationships
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


# generate the complete path from all of the contour families
def generate_path(family_list, line_thickness = 1, angle = np.pi/7):

    total_path = []

    total_start = datetime.datetime.now()

    for index, family in enumerate(family_list):
        start = datetime.datetime.now()
        total_path.append(family.generate_total_path(line_thickness, angle))
        logging.info("FAMILY: "+str(index) + "\t" + str(datetime.datetime.now() - start))

    logging.info("TOTAL TIME: " + str(datetime.datetime.now() - total_start))

    return total_path 


# plot all of the paths in total path
def plot_paths(total_path, contour_list):

    for contour in contour_list:
        X,Y = contour.plot()
        plt.plot(X,Y)


    X = []
    Y = []

    for family_path in total_path:

        for path in family_path:

            X.append([])
            Y.append([])
            for point in path:
                X[-1].append(point.x)
                Y[-1].append(point.y)
        
    for x,y in zip(X,Y):
        plt.plot(x,y)

    plt.show()


# execute the contour fill on the image
def execute(image):
    # create the border lines for each contour
    contour_list = generate_border_lines(image)

    # organize contours into families of contours
    family_list = create_contour_families(contour_list)
    
    # generate the paths
    total_path = generate_path(family_list)

    # plot the paths
    plot_paths(total_path, contour_list)


if __name__ == "__main__":
    main()
