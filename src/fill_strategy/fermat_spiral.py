'''
Methods for generating fermat spirals from input spirals

@author ejbosia
'''

from shapely.geometry import Point, LineString

from utilities.shapely_utilities import cut, reverse

from fill_strategy.spiral import SpiralGenerator, calculate_endpoint


class FermatSpiral:

    def __init__(self, spiral, distance):
        self.path = self._convert_spiral(spiral, distance)

    def _convert_spiral(self, spiral, distance):
        path = self._outer_spiral(spiral.contours, distance)

        return path

    def _outer_spiral(self, contours, distance):

        path = []

        # loop through the even spirals ~ the outer most spiral is the outer spiral
        for i in range(0, len(contours), 2):

            contour = LineString(contours[i])
           
            # get the reroute point away from the end towards start
            reroute = calculate_endpoint(contour, distance)
            cut_path, _ = cut(contour, contour.project(reroute))
            path.extend(list(cut_path.coords))

            # return if there are no more inner paths
            if i+1 >= len(contours):
                return path

            # the odd spiral piece goes from the projection point to the end
            contour_inner = LineString(contours[i+1])
            distance = contour_inner.project(reroute)
            _,cut_path = cut(contour_inner, distance)

            # if there is no cut path, only add the last point
            if cut_path is not None:
                path.extend(list(cut_path.coords))
            else:
                path.append(list(contour_inner.coords[-1]))
        return path

    def _inner_spiral(self, contours, distance):

        path = []

        # get the last "odd" index
        length = len(contours)
        last_index = length if length % 2 == 1 else length - 1

        # loop backwards through the odd values
        for i in range(last_index, 0, 2):

            contour = reverse(LineString(contours[i]))
            reroute = calculate_endpoint(contour, distance)
            cut_path, _ = cut(contour, contour.project(reroute))
            path.append(list(cut_path.coords))

            # the odd spiral piece goes from the projection point to the end
            contour_inner = reverse(LineString(contours[i-1]))
            end_point = Point(cut_path.coords[-1])
            _, cut_path = cut(contour_inner, contour_inner.project(end_point))

            path.append(list(cut_path.coords))

        return path

    def get_path(self):
        return self.path


class FermatSpiralGenerator:

    def __init__(self, polygons, distance, borders=0, connected=False):
        self.polygons = polygons
        self.distance = distance
        self.borders = borders
        self.connected = connected

    def generate(self):

        # generate spirals and convert to fermat spirals
        spirals = SpiralGenerator(self.polygons, self.distance, self.borders).generate()
        output = [FermatSpiral(spiral, self.distance) for spiral in spirals]
        print(output)
        return output
