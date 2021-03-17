'''
Convert an input image into polygons
'''

import cv2
import numpy as np
from shapely.geometry import Point, LineString, LinearRing, Polygon

# return a tuple of contour points and heirarchy
def generate_border_lines(image):

    contours,heirarchy = cv2.findContours(image, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)  

    contour_list = []

    for contour,heirarchy in zip(contours, heirarchy[0]):
        vertex_list = []
        for c in contour:
            vertex_list.append(tuple(c[0]))

        contour_list.append((vertex_list,heirarchy))

    return contour_list


# get all of the children of the parent contour
def get_children(contour_list, parent_contour):

    child_list = []

    first_child_index = parent_contour.heirarchy[2]
    child = contour_list[first_child_index]
    child_list.append(child)


    # loop while there are more children
    while not child[1][0] == -1:
        next_child_index = child[1][0]
        child = contour_list[next_child_index]
        child_list.append(child[0])
    
    # return the list of children
    return child_list



# combine contours into single level parent-children relationships
def create_polygons(contour_list):

    polygon_list = []

    # find the first parent contour
    for contour in contour_list:

        h = contour[1]

        # start with a parent contour
        if h[3] == -1:

            # if there are no children, create an empty family with only the parent contour
            if h[2] == -1:
                child_list = []
            # otherwise, find all of the children
            else:
                child_list = get_children(contour_list, contour)

            polygon_list.append(Polygon(contour[0], holes=child_list))

    return polygon_list


'''
Convert an image into Shapley polygons
'''
def execute(image):

    contours = generate_border_lines(image)

    return create_polygons(contours)