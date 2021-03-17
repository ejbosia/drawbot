'''
Contour Fill
This file contains the logic for creating a contour fill of a black and white image

@author ejbosia
'''

import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
import math

import convert_polygons as cp

from shapely.geometry import Point, LineString, LinearRing, Polygon, MultiLineString
from shapely.affinity import rotate

import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

import gcode as GC

'''
Generate the intersection points using horizontal lines on the polygon
'''
def generate_intersection_points(polygon, distance):

    l1 = LineString(list(polygon.envelope.exterior.coords)[0:2])
    
    # move l1 half the distance to start the fill
    l1 = l1.parallel_offset(distance/2, 'left')

    intersection_list = []

    intersection_contours = []

    # loop while the line intersects the polygon
    while l1.intersects(polygon):
        
        intersection_points = polygon.exterior.intersection(l1)

        intersection_list.append(list(intersection_points))
        
        l1 = l1.parallel_offset(1, 'left')    

    '''
    Flatten and sort the contour points
    TODO will want to convert this to work with interiors
    '''
    row_points = []

    for row in intersection_list:
        row_points.extend(row)
        
    # sort the points on the distance from the start
    row_points.sort(key=polygon.exterior.project)

    intersection_contours = [row_points]

    return intersection_list, intersection_contours





# remove peaks from the points
def remove_peaks(intersection_list, row_points):

    # check every point for peaks
    peaks = []
    new_points = []

    # get the previous and next points
    rp0 = row_points[-1:] + row_points[0:-1]
    rp1 = row_points
    rp2 = row_points[1:] + row_points[0:1]

    for p0, p1, p2 in zip(rp0,rp1,rp2):
        
        # remove the point if the other two points are at the same level
        if p0.y == p2.y:
            peaks.append(p1)
            row_points.remove(p1)            

    # remove the peaks from the intersection list
    for p in peaks:
        for index, row in enumerate(intersection_list):
            if p in row:
                intersection_list[index].remove(p)

    return intersection_list, row_points


'''
Get the next point up the polygon
'''
def next_point(point, ring, new_row):
    
    i1 = ring.index(point)
    
    i0 = i1-1
    i2 = i1+1
    
    # loop i2 around the ring if needed
    if i2 == len(ring):
        i2 = 0
    
    # check the previous point
    if ring[i0] in new_row: return ring[i0]
    
    # check the next point
    if ring[i2] in new_row: return ring[i2]    
    
    # if neither point returns
    return None


'''
Get the point across polygon
'''
def across_point(point, row):
    
    index = row.index(point)
    
    if index % 2 == 0:
        return row[index+1]
    else:
        return row[index-1]


# find a point not in the path
def get_available_pt(total_path, intersection_list):
    
    mls = MultiLineString([LineString(p) for p in total_path])
    
    for row in intersection_list:
        
        for p in row:
            
            if mls.intersects(p):
                continue
            else:
                return p
    return None


'''
Generate the path for one of the polygons
'''
def generate_path(polygon, line_thickness = 1, angle = np.pi/7):

    total_path = []

    # rotate
    polygon = rotate(polygon, -angle, use_radians=True)
    
    # get the intersection points
    intersection_list, intersection_contours = generate_intersection_points(polygon, line_thickness)

    
    # generate the paths until no points remain
    start = get_available_pt([], intersection_list)

    total_path = []
    while not start is None:
        
        total_path.append(fill_path(start, intersection_list, row_points))
        start = get_available_pt(total_path, intersection_list)

    # rotate the path back
    
    return total_path


'''
Generate the complete path from all of the contour families
'''
def generate_total_path(polygon_list, line_thickness = 1, angle = np.pi/7):

    total_path = []

    total_start = time.time()

    for index, polygon in enumerate(polygon_list):
        start = time.time()
        total_path.append(generate_path(polygon, line_thickness, angle))

    logging.info("TOTAL TIME: " + str(time.time() - total_start))

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
    # organize contours into families of contours
    polygon_list = cp.execute(image)
    
    # generate the paths
    total_path = generate_path(polygon_list)

    # plot the paths
    plot_paths(total_path, contour_list)



if __name__ == "__main__":
    main()
