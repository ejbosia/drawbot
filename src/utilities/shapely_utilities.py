'''
Utility functions to use with Shapely geometry objects

@author ejbosia
'''

from shapely.geometry import Point, LineString
from shapely.geometry import CAP_STYLE, JOIN_STYLE

from matplotlib import pyplot


def distance_transform(polygon, distance):
    '''
    Apply a distance transform to the polygon
        Parameters:
            polygon (Polygon)
            distance (float)
        Returns:
            result (list of LinearRing)
    '''
    if polygon.is_empty:
        return []

    temp = polygon.exterior.buffer(distance, cap_style=CAP_STYLE.flat, join_style=JOIN_STYLE.mitre)

    polygon = polygon.difference(temp)

    if polygon.is_empty:
        return []

    result = []

    # MultiPolygons are the result of concave shapes ~ distance transform creates multiple polygons
    if polygon.type == "MultiPolygon":
        for p in polygon:
            result.append([p.exterior])
            result[-1].extend(distance_transform(p, distance))
    else:
        result.append(polygon.exterior)
        result.extend(distance_transform(polygon, distance))

    return result


def plot_poly(polygon):
    '''
    Plot all of the contours of an input polygon
    '''
    pyplot.plot(*polygon.exterior.xy)

    for i in polygon.interiors:
        pyplot.plot(*i.xy)


def plot_contours(result):
    '''
    Plot all of the contours in the result of a distance transform
    '''
    for p in result:
        if type(p) is list:
            plot_contours(p)
        else:
            plot_poly(p)


def cut(line, distance):
    '''
    Cut a linestring at a specified distance
        Parameters:
            line (LineString)
            distance (float)
        Returns:
            [LineString, LineString] or [None, LineString] or [LineString, None]
    '''

    # Cuts a line in two at a distance from its starting point
    if distance <= 0.0:
        return [None, LineString(line)]
    elif distance >= line.length:
        return [LineString(line), None]

    coords = list(line.coords)
    for i, p in enumerate(coords):
        pd = line.project(Point(p))
        if pd == distance:
            return [
                LineString(coords[:i+1]),
                LineString(coords[i:])]
        if pd > distance:
            cp = line.interpolate(distance)
            return [
                LineString(coords[:i] + [(cp.x, cp.y)]),
                LineString([(cp.x, cp.y)] + coords[i:])]
    # this is between the last point
    # this is to catch for linear rings (last point projection is 0)
    cp = line.interpolate(distance)
    return [
        LineString(coords[:-1] + [(cp.x, cp.y)]),
        LineString([(cp.x, cp.y)] + [coords[-1]])]


def cycle(contour, distance):
    '''
    Reformat the linestring so position 0 is the start point.
    This may involve inserting a new point into the contour.
        Parameters:
            contour (LineString)
            distance (float)
        Returns:
            points (LineString)
    '''
    # force the distance to within the contour
    distance = distance % contour.length

    # cut the contour at the projection distance
    result = cut(contour, distance)

    if result[0] is None or result[1] is None:
        points = list(contour.coords)
    else:
        [ls1, ls2] = result
        points = list(ls2.coords) + list(ls1.coords)

    return LineString(points)


def self_intersections(ls):
    '''
    Find any self intersections in the input linestring
        Parameters:
            ls (LineString)
        Returns:
            intersection_points (list of Point)
    '''
    intersection_points = []

    for i in range(len(ls.coords)-3):

        p0 = ls.coords[i]
        p1 = ls.coords[i+1]

        remaining_path = LineString(ls.coords[i+2:])
        test = LineString([p0, p1])

        # check for intersection only with the linestring coords 2 past the start (the next line cannot intersect with the current line)
        if test.intersects(remaining_path):

            intersections = test.intersection(remaining_path)

            if intersections.type == "Point":
                intersection_points.append(intersections)
            else:
                for p in intersections:
                    intersection_points.append(p)

    return intersection_points


def self_intersections_binary(ls):

    '''
    Find any self intersections in the input linestring using binary search like recursion
        Parameters:
            ls (LineString)
        Returns:
            intersection_points (list of Point)
    '''
    intersection_points = []

    pivot = int(len(ls.coords)/2)

    ls1_coords = ls.coords[:pivot]
    ls2_coords = ls.coords[pivot:]

    ls1 = LineString(ls1_coords) if len(ls1_coords) > 1 else LineString()
    ls2 = LineString(ls2_coords) if len(ls1_coords) > 1 else LineString()

    s0 = ls.is_simple
    s1 = ls1.is_simple
    s2 = ls2.is_simple

    # if s0 is complex, but its bisects are simple, run the normal self intersection algorithm on s0
    if not s0 and s1 and s2:
        return self_intersections(ls)
    if not s1:
        intersection_points.extend(self_intersections_binary(ls1))
    if not s2:
        intersection_points.extend(self_intersections_binary(ls2))

    return intersection_points


def reverse(ls):
    '''
    Reverse a input linestring
        Parameters:
            ls (LineString)
        Returns:
            LineString
    '''
    return LineString(ls.coords[::-1])


def merge(ls1, ls2):
    '''
    Merge two linestrings
        Parameters:
            ls1 (LineString)
            ls2 (LineString)
        Returns:
            LineString
    '''
    return LineString(list(ls1.coords) + list(ls2.coords))


def sample(ls, distance):
    '''
    Evenly sample the linestring
        Parameters:
            ls (LineString)
            distance (float)
        Returns:
            LineString: coordinates are sample points
    '''
    pos = 0

    points = []

    while pos < ls.length:
        points.append(ls.interpolate(pos))

        pos += distance

    return LineString(points)


def virtual_boundary(polygon, distance):
    '''
    Create a virtual boundary around a polygon
        Parameters:
            polygon (Polygon)
            distance (float)
    '''
    virtual_polygon = polygon.buffer(distance)

    exterior = list(virtual_polygon.exterior.coords)

    interiors = [list(interior.coords) for interior in virtual_polygon.interiors]

    return exterior, interiors


def curvature(ls):
    '''
    Generate the curvature of each vertex on a linestring
    Raises:
        NotImplementedError
    '''
    raise NotImplementedError("Curvature calculations has not been implemented yet")


def adaptive_sample(ls, K=1):
    '''
    Adaptively sample the linestring based on the curvature of each vertex ~ this returns a new list of points
    Raises:
        NotImplementedError
    '''
    raise NotImplementedError("Adaptive sampling has not been implemented")
