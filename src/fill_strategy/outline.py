'''
Outline
Generate the outline path of a list of polygons

@author ejbosia
'''
class Outline:

    def __init__(self, polygon):
        self.path = self.generate_outline(polygon)

    def _generate_outline(self, polygon):
        path = [list(polygon.exterior.coords)]
        
        for interior in polygon.interiors:
            path.append(list(interior.coords))

        return path

    def get_path(self):
        return self.path


class OutlineGenerator:

    def __init__(self, polygons):
        self.polygons = polygons

    def generate(self):
         total_path = []

        for polygon in polygons:
            total_path.extend(outline_polygon(polygon))

        return total_path
