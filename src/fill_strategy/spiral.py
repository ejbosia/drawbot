'''
Generate a space-filling spiral path on an input polygon

@author ejbosia
'''

from shapely.geometry import Point, LineString

from utilities.shapely_utilities import distance_transform, cut, cycle

class Spiral:
    '''
    Spiral Class
   
    Args
    ----
    contours: contours
    distance: float
   
    Attributes
    ----------
    contours: list of shapely.geometry.LineString
    
    Methods
    -------
    get_path()
        Output the path as a list of points
    '''

    def __init__(self, contours, distance):

        if distance <= 0:
            raise ValueError("SPIRAL DISTANCE MUST BE GREATER THAN 0")
        
        if not contours:
            raise ValueError("NO CONTOURS INPUT")

        self.contours = self._generate_spiral(contours, distance)


    def _generate_spiral(self, contours, distance):
        '''
        Generate the spiral
        
        Parameters
        ----------
        contours: list of shapely.geometry.LineString
        distance: float
        
        Returns
        -------
        spiral_contours: list of shapely.geometry.LineString
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
        
        Returns
        -------
        path: list of points
        '''

        path = [c for contour in self.contours for c in contour.coords]
        
        path = list(dict.fromkeys(path))

        return path


class SpiralGenerator:
    '''
    Converts a list of Polygons into a list of Spiral

    Args
    ----------
    polygons: list of shapely.geometry.Polygon
    distance: float
    boundaries: int, optional

    Attributes
    ----------
    polygons: list of shapely.geometry.Polygon
    distance: float
    boundaries: int

    Methods
    -------
    generate()
        Generate the spirals from a list of Polygons
    '''

    def __init__(self, polygons, distance, boundaries=0):
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
        
        Returns
        -------
        spirals: list of Spiral
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
        
        Parameters
        ----------
        contours: list of list of ... LineString
        
        Returns
        -------
        format_list: list of LineString
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
    
    Parameters
    ----------
    contour: shapely.geometry.LineString
    radius: float
    
    Returns:
    point: shapely.geometry.Point
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
    

    distance_ring = start.buffer(radius).exterior
    line = LineString(points[index-1:index+1])

    # the return of this must be a point
    point = distance_ring.intersection(line)

    return point
