'''Contains classes for the creating an Outline'''


class Outline:
    '''
    Outline Class

    Args
    ----
    perimeter: shapely.geometry.LineString

    Attributes
    ----------
    path: list of shapely.geometry.Point

    Methods
    -------
    get_path()
        Output the path as a list of points
    '''

    def __init__(self, perimeter):
        self.path = list(perimeter.coords)

    def get_path(self):
        '''
        Return the path of the outline

        Returns
        -------
        list of tuples
        '''
        return self.path


class OutlineGenerator:
    '''
    OutlineGenerator Class

    Args
    ----
    polygons: list of shapely.geometry.Polygon

    Attributes
    ----------
    polygons: list of shapely.geometry.Polygon

    Methods
    -------
    generate()
        Create a list of Outline objects from the polygons
    '''

    def __init__(self, polygons):
        self.polygons = polygons

    def generate(self):
        '''
        Create a list of Outline objects from the polygons

        Returns
        -------
        list of Outline
        '''

        total_path = []

        for polygon in self.polygons:

            total_path.append(Outline(polygon.exterior))

            for interior in polygon.interiors:
                total_path.append(Outline(interior))

        return total_path
