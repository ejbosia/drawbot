'''
Contour Fill
This file contains the logic for creating a contour fill of a black and white image

@author ejbosia
'''

import numpy as np

from shapely.geometry import Point, LineString, LinearRing, Polygon, MultiLineString
from shapely.affinity import rotate

import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

import warnings

from numba import jit

class ZigZag:

    '''
    '''
    def __init__(self, start_index, all_points, contour_indices, available):
        self.path = ZigZag._generate_zigzag(start_index, all_points, contour_indices, available)

    '''
    '''
    @jit(nopython=True)  
    def _generate_zigzag(start_index, all_points, contour_indices, available):    

        path = []    
        
        p1 = all_points[start_index]
        available[start_index] = False
                
        while not p1 is None:
            
            path.append(p1)
            i2 = across_point(p1, all_points)
            available[i2] = False
            p2 = all_points[i2]
            
            path.append(p2)
            p1 = next_point(p2, contour_indices, all_points, available)    

        return path

    '''
    Output the path as a list of points
    '''
    def get_path(self):
        return self.path

'''
Generate a list of Spirals from a list of polygons
'''
class ZigZagGenerator:

    def __init__(self, polygons, distance, boundaries=0, angle=np.pi/6):

        if not polygons:
            raise ValueError("POLYGONS IS EMPTY")
        if distance <= 0:
            raise ValueError("DISTANCE IS 0 OR NEGATIVE")

        self.polygons = polygons
        self.distance = distance
        self.boundaries = 0
        self.angle = angle


    '''
    Generate the complete path from all of the contour families
    '''
    def generate(self):

        zigzags = []

        for i, polygon in enumerate(self.polygons):

            polygon = rotate(polygon, self.angle, use_radians=True)

            intersections, contour_indices = self._generate_intersections(polygon, self.distance)

            if intersections.shape[0] != 0:
                zigzags.extend(self._generate_path(intersections, contour_indices))

        return zigzags 


    '''
    Generate all intersections (and contour indices) for an input polygon
    '''
    def _generate_intersections(self, polygon, distance):
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
    Generate the path for one of the polygons
    '''
    def _generate_path(self, all_points, contour_indices):

        total_path = []
        
        sort_index = all_points[:,1].argsort()

        # array that stores available points
        available = np.ones(all_points.shape[0], bool)
                
        while available.any():

            total_path.append(
                ZigZag(
                    sort_index[np.argmax(available[sort_index])],
                    all_points, 
                    contour_indices, 
                    available
                )
            )

        return total_path


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


'''
Get the next point up the polygon
'''
@jit(nopython=True) 
def next_point(point, contour_indices, all_points, available):
        
    i1 = np.where((all_points[:,0] == point[0]) & (all_points[:,1]==point[1]))[0][0]
    
    i0 = i1-1
    i2 = i1+1    
    
    if i0+1 in contour_indices:
        i0 = contour_indices[np.where((i0+1) == contour_indices)[0][0]+1] -1
    elif i2 in contour_indices:
        i2 = contour_indices[np.where(i2 == contour_indices)[0][0]-1]
        
    # check the previous point
    if available[i0] and all_points[i0][1] > point[1]:
        available[i0] = False
        return all_points[i0]
    
    # check the next point
    if available[i2] and all_points[i2][1] > point[1]:
        available[i2] = False
        return all_points[i2]   
    
    # if neither point returns
    return None


'''
Get the point across polygon
'''
@jit(nopython=True) 
def across_point(point, all_points): 

    index = (all_points[:,1]==point[1]).nonzero()[0]
    row = all_points[index][:,0]

    # sort the row
    row_sort = row.argsort()

    index = index[row_sort]
    row = row[row_sort]
        
    i = np.where((row == point[0]))[0][0]
        
    if i % 2 == 0:
        return index[i+1]
    else:
        return index[i-1]