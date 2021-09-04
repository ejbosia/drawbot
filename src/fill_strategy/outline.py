'''
Outline
Generate the outline path of a list of polygons

@author ejbosia
'''
class Outline:

    def __init__(self, perimeter):
        self.path = list(perimeter.coords)

    def get_path(self):
        return self.path


class OutlineGenerator:

    def __init__(self, polygons):
        self.polygons = polygons

    def generate(self):
        total_path = []

        for polygon in self.polygons:

            total_path.append(Outline(polygon.exterior))

            for interior in polygon.interiors:
                total_path.append(Outline(interior))

        return total_path
