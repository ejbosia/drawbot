'''
Generate a space-filling spiral path on an input polygon

@author ejbosia
'''

from src.utilities.shapely_utilities import distance_transform, cut, cycle, self_intersections_binary, reverse

from shapely.geometry import Point, LineString, Polygon

import numpy as np


class Spiral:
    '''
    Spiral Class
    This stores the components that make a spiral ~ a list of separate paths that can be formatted into a full path.
    '''

    def __init__(self, contours, distance):
        '''
        Initialize the spiral
            Parameters:
                contours (list of contours)
                distance (float)
        '''
        if distance <= 0:
            raise ValueError("SPIRAL DISTANCE MUST BE GREATER THAN 0")
        
        if not contours:
            raise ValueError("NO CONTOURS INPUT")

        self.contours = self._generate_spiral(contours, distance)


    def _generate_spiral(self, contours, distance):
        '''
        Generate the spiral
            Parameters:
                contours (list of contours)
                distance (float)
            Returns
                spiral_contours (list of contours)
        '''
        spiral_contours = []
        end = None

        # find the start and end point of each contour
        for contour in contours:

            # if there is a previous end point, find the start using this end point
            if not end is None:

                # set the start of the contour to the closest point to the end point
                contour = cycle(contour, contour.project(end))

            end = calculate_endpoint(contour, distance)

            # if there is a new valid end point, cut the contour and save the piece between the start and end point
            if not end is None:
                spiral_contours.append(cut(contour, contour.project(end))[0])

        return spiral_contours


    def get_path(self):
        '''
        Get the total path of the spiral
            Returns:
                path (list of points)
        '''

        path = [c for contour in self.contours for c in contour.coords]
        
        path = list(dict.fromkeys(path))

        return path


class SpiralGenerator:
    '''
    Converts a list of Polygons into a list of Spirals
    '''

    def __init__(self, polygons, distance, boundaries=0):
        '''
        Initialize the SpiralGenerator object
            Parameters:
                polygons (list of Polygon)
                distance (float)
                boundaries (int)
        '''
        if not polygons:
            raise ValueError("POLYGONS IS EMPTY")
        if distance <= 0:
            raise ValueError("DISTANCE IS 0 OR NEGATIVE")

        self.polygons = polygons
        self.distance = distance
        self.boundaries = 0


    def generate(self):
        '''
        Generate the spirals from the list of Polygons
            Returns:
                spirals (list of Spiral)
        '''
        spirals = []

        for polygon in self.polygons:
            
            # get the isocontours
            contours = distance_transform(polygon, self.distance)
            contours = self._flatten(contours)
            
            # initialize a spiral for each set of contours
            for c in contours:
                spirals.append(Spiral(c, self.distance))

        return spirals

    def _flatten(self, contours):
        '''
        Flatten the arbitrarily deep list of lists of contours into a list of contours
            Parameters:
                contours (list of list of ... contours)
            Returns:
                format_list (list of contours)
        '''        
        format_list = []
        temp = []

        for c in contours:
            if type(c) is list:
                format_list.extend(self._flatten(c))
            else:
                temp.append(c)
        
        format_list.append(temp)       
        
        return format_list


def calculate_endpoint(contour, radius):
    '''
    Find the point a distance away from the end of the contour
        Parameters:
            contour (LineString)
            radius (float)
        Returns:
            point (Point)
    '''    
    # reverse the contour coords to loop backwards through them
    points = contour.coords[::-1]

    start = Point(points[0])

    # find the first distance past the position (all previous will be before the position)
    for i, p in enumerate(points):
        
        dis = start.distance(Point(p))

        if dis > radius:
            index = i
            break
    else:
        return None

    # set the index correctly to match reverse
    i1 = index
    i0 = (index-1)

    # we know the intersection must be on this line, and there can only be one
    distance_ring = start.buffer(radius).exterior
    line = LineString(points[i0:i1+1])

    # the return of this must be a point
    point = distance_ring.intersection(line)

    return point
