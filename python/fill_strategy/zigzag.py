'''
Contour Fill
This file contains the logic for creating a contour fill of a black and white image

@author ejbosia
'''

import numpy as np
import time

from shapely.geometry import Point, LineString, LinearRing, Polygon, MultiLineString
from shapely.affinity import rotate

import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

from numba import jit

'''
Generate the intersection points using horizontal lines on the polygon
'''
@jit(nopython=True)
def generate_intersections_contour(vertex_list, distance):
    
    intersections = []
    
    for i in range(len(vertex_list)-1):        
        p0 = vertex_list[i]
        p1 = vertex_list[i+1]
        
        dx = p1[0] - p0[0]
        dy = p1[1] - p0[1]
        
        if dy == 0:
            continue
            
        dxdy = dx/dy
        
        if p0[1] < p1[1]:
            indices = range(np.ceil(p0[1]/distance), np.ceil(p1[1]/distance))            
        else:
            indices = range(int(p0[1]/distance), int(p1[1]/distance), -1)

                        
        for j in indices:

            index = j * distance - p0[1]
            
            x = dxdy * index + p0[0]
            y = index + p0[1]

            intersections.append((x,y))
            
    return np.array(intersections)


# find peaks numba
@jit(nopython=True)
def remove_peaks(contour, intersections, mask):
    
    end = len(intersections)-1
    
    end = len(contour)
    # check if the points are on the vertex list
    for c in range(len(contour)):
        
        p1 = contour[c]
        
        # if the point is in intersections, check the previous and next point
        if ((p1[0] == intersections[:,0]) & (p1[1] == intersections[:,1])).any():
            
            p0 = contour[(c-1)%end]
            p2 = contour[(c+1)%end]
            
            d0 = p0[1]-p1[1]
            d2 = p2[1]-p1[1]
            
            # handle plateaus
            if d0 == 0:
                p0 = contour[(c-2)%end]
                d0 = p0[1]-p1[1]

            if d2 == 0:
                p2 = contour[(c+2)%end]
                d2 = p2[1]-p1[1]
                
            
            # check if the points are on the same or opposite sides of x axis through point p1
            sign = d2 * d0
            
            # sign >= 0 ~ points are on same side ~ peak
            if sign > 0:
                
                # find p1 in intersections
                index = np.where((p1[0] == intersections[:,0]) & (p1[1] == intersections[:,1]))[0][0]
                mask[index] = False

    return intersections[mask,:]


'''
Generate all intersections (and contour indices) for an input polygon
'''
def generate_intersections(polygon, distance):

    contour_indices = [0]
    all_points = []
    sum = 0

    vertex_list = np.array(list(polygon.exterior.coords)) 
    intersections = generate_intersections_contour(vertex_list, distance)
    intersections = remove_peaks(vertex_list, intersections, np.ones(intersections.shape[0], bool))

    sum += len(intersections)

    all_points.extend(intersections)
    contour_indices.append(sum)

    for interior in polygon.interiors:
        vertex_list = np.array(list(interior.coords)) 
        intersections = generate_intersections_contour(vertex_list, distance)
        intersections = remove_peaks(vertex_list, intersections, np.ones(intersections.shape[0], bool))

        sum += len(intersections)

        all_points.extend(intersections)
        contour_indices.append(sum)

    return np.array(all_points), np.array(contour_indices)

'''
Get the next point up the polygon
'''
@jit(nopython=True) 
def next_point(point, contour_indices, all_points):
        
    i1 = np.where((all_points[:,0] == point[0]) & (all_points[:,1]==point[1]))[0][0]
    
    i0 = i1-1
    i2 = i1+1    
    
    if i0+1 in contour_indices:
        i0 = contour_indices[np.where((i0+1) == contour_indices)[0][0]+1] -1
    elif i2 in contour_indices:
        i2 = contour_indices[np.where(i2 == contour_indices)[0][0]-1]
        
    # check the previous point
    if all_points[i0][1] > point[1]:
        return all_points[i0]
    
    # check the next point
    if all_points[i2][1] > point[1]:
        return all_points[i2]    
    
    # if neither point returns
    return None


'''
Get the point across polygon
'''
@jit(nopython=True) 
def across_point(point, all_points): 

    row = all_points[all_points[:,1]==point[1]][:,0]
    row.sort()
        
    index = np.where((row == point[0]))[0][0]
        
    if index % 2 == 0:
        return np.array([row[index+1], point[1]])
    else:
        return np.array([row[index-1], point[1]])


'''
Find an intersection point that is not in the path
'''
@jit(nopython=True)
def get_available_pt_index(last_start,total_path, all_points):   

    for i in range(last_start, len(all_points)):
        if ((total_path[:,0] == all_points[i,0]) & (total_path[:,1] == all_points[i,1])).any():
            continue
        else:
            return i
    
    return -1   


'''
Generate path until completion
'''
@jit(nopython=True)  
def fill_path(start_index, all_points, contour_indices):    
        
    p1 = all_points[start_index]
    
    path = []
    
    while not p1 is None:
        
        path.append(p1)
        p2 = across_point(p1, all_points)
        
        path.append(p2)
        p1 = next_point(p2, contour_indices, all_points)    
            
    return path


'''
Generate the path for one of the polygons
'''
def generate_path(all_points, contour_indices):

    total_path = []
    temp = []
    start_index = 0
    
    sort_points = all_points[all_points[:,1].argsort()]
        
    last_start = 0
    
    while last_start != -1:

        path = fill_path(start_index, all_points, contour_indices)
                
        temp.extend(path)
        
        last_start = get_available_pt_index(last_start, np.array(temp), sort_points)
                
        if last_start != -1:
            start_point = sort_points[last_start]

            # get the start index in all points
            start_index = np.where((all_points[:,0]==start_point[0]) & (all_points[:,1]==start_point[1]))[0][0]

        total_path.append(path)

    return total_path


'''
Generate the complete path from all of the contour families
'''
def generate_total_path(polygon_list, distance = 1, angle = np.pi/7):

    total_path = []

    total_start = time.time()

    for i, polygon in enumerate(polygon_list):
        start = time.time()

        intersections, contour_indices = generate_intersections(polygon, distance)

        if intersections.shape[0] != 0:
            total_path.append(generate_path(intersections, contour_indices))
            
            logging.info("Polygon: " + str(i) + ": " + str(time.time() - start))
    logging.info("TOTAL TIME: " + str(time.time() - total_start))

    return total_path 



# execute the contour fill on the image
def execute(polygons, distance):

    # generate the paths
    total_path = generate_total_path(polygons, distance=distance)

    return total_path
