'''
drawbot
This is the entry module to the program. It links the components together.


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


def fill_contours(contour_list, line_thickness=1, angle=math.pi/3):

    start_point = contour_list[1].find_maximum_point(angle-(np.pi/2))
    plt.scatter(start_point[0],start_point[1])

    traverse_amount = -line_thickness

    perpendicular_angle = angle + (np.pi/2)

    dx = np.cos(perpendicular_angle)
    dy = np.sin(perpendicular_angle)

    start_point = (dx*line_thickness+start_point[0], dy*line_thickness+start_point[1])

    create_path(contour_list, line_thickness, angle, contour_list[1], start_point)



# generate the complete path from all of the contour families
def generate_path(image, line_thickness = 6, angle = np.pi/6):

    total_path = []

    total_start = datetime.datetime.now()

    for index, family in enumerate(family_list):
        start = datetime.datetime.now()
        total_path.append(family.generate_total_path(line_thickness, angle))
        plogging.info("FAMILY: "+str(index) + "\t" + str(datetime.datetime.now() - start))

    plogging.info("TOTAL TIME: " + str(datetime.datetime.now() - total_start))

    return total_path 


# plot all of the paths in total path
def plot_paths(total_path):
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


def main(file="picture.png", inverse=False, resize = 8):
    print(file)

    image = cv2.imread(file, 0)

    image = cv2.resize(image, None, fx=resize, fy=resize, interpolation=cv2.INTER_NEAREST)

    if inverse:
        image = 255-image

    # organize contours into families of contours
    family_list = create_contour_families(contours)
    
    # generate the paths
    total_path = generate_path(family_list)

    # plot the paths
    plot_paths(total_path)
    

if __name__ == "__main__":
    main()
