'''
Take in a path and extract different metrics from the path
'''

import numpy as np
from shapely.geometry import LineString, MultiPolygon


class Metrics:

    def __init__(self, segments=True, commands=True, curvature=False, underfill=False, overfill=False):

        self.segments = segments
        self.commands = commands
        self.curvature = curvature
        self.underfill = underfill
        self.overfill = overfill

    def measure_commands(self, total_path):
        '''
        Count the number of commands needed to run the total path
        '''
        commands = 0

        for path in total_path:
            commands += len(path.get_path())

        return commands

    def neighbors(self, i1, length):
        '''
        Get the neighbor indices with wrap around
        '''
        i0 = i1-1 if i1 != 0 else length-1
        i2 = i1+1 if i1+1 != length else 0

        return i0, i1, i2

    def _path_curvature(self, path):
        '''
        Calculate average angle change of the path
        '''
        sharpness = 0

        for i1 in range(len(path)):

            i0, i1, i2 = self.neighbors(i1, len(path))

            p0 = path[i0]
            p1 = path[i1]
            p2 = path[i2]

            a0 = np.arctan2(p1[1]-p0[1], p1[0]-p0[0])
            a2 = np.arctan2(p2[1]-p1[1], p2[0]-p1[0])

            # get the angle change
            da = a2-a0

            sharpness += abs(da)

        return sharpness

    def measure_curvature(self, total_path):
        '''
        Get the total angle change. This should be directly comparable between paths
        '''
        sharpness = 0

        for path in total_path:
            sharpness += self._path_curvature(np.array(path))

        return sharpness

    def measure_underfill(self, total_path, polygons, distance, epsilon=0.0000001):
        '''
        Find "underfill" areas of the polygon ~ returns a percentage from the total
        '''

        # create a multipolygon from polygons
        fill_polygons = MultiPolygon(polygons)
        fill_area = fill_polygons.area

        # get all of the path fills
        path_areas = [LineString(path).buffer(distance/2+epsilon) for path in total_path]

        # get the area of the difference ~ these are the remaining areas of the starting polygon that are not filled
        for path_area in path_areas:
            fill_polygons = fill_polygons.difference(path_area)

        return fill_polygons.area/fill_area

    def measure_overfill(self, total_path, distance):
        '''
        Find "overfill" areas of the polygon ~ returns a percentage from the total
        '''

        ideal = 0
        actual = 0

        # calculate the area difference
        for path in total_path:

            # ideal path area with no overlap
            ideal += LineString(path).length * distance

            # actual path area
            actual += LineString(path).buffer(distance/2, cap_style=2, join_style=2).area

        '''
        calculate the overfill
         - the ideal area assumes each line segment is a rectangle. Even changing angles preserve the area of the line segments
         - the actual area calculates the rectangular buffer of the path. Overlapped areas are merged, meaning the area is lowered by one of the overlap areas
         - to get the true overlap, the area of the overlap needs to be doubled
        '''
        overlap = ideal - actual

        return overlap * 2 / ideal

    def measure(self, total_path, filename, method, distance, polygons=None):
        '''
        Return a dictionary of measurements. Unused measurements are returned as np.Nan
        '''
        assert type(distance) is float or type(distance) is int

        if self.underfill:
            assert polygons is not None

        measurements = {
            "Filename": filename,
            "Method": method,
            "Distance": distance,
            "Segments": np.nan,
            "Commands": np.nan,
            "Curvature": np.nan,
            "Underfill": np.nan,
            "Overfill": np.nan,
        }

        if self.segments:
            measurements["Segments"] = len(total_path)
        if self.commands:
            measurements["Commands"] = self.measure_commands(total_path)
        if self.curvature:
            raise NotImplementedError
        if self.underfill:
            measurements["Underfill"] = self.measure_underfill(total_path, polygons, distance)
        if self.overfill:
            measurements["Overfill"] = self.measure_overfill(total_path, distance)
        return measurements
