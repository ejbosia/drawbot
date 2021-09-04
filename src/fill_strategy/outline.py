'''
Outline
Generate the outline path of a list of polygons

@author ejbosia
'''

'''
Get the outline of the input polygon
'''
def outline_polygon(polygon):

    path = [list(polygon.exterior.coords)]
    
    for interior in polygon.interiors:
        path.append(list(interior.coords))

    return path


# execute the contour fill on the image
def execute(polygons, distance):

    total_path = []

    for polygon in polygons:
        total_path.extend(outline_polygon(polygon))

    return total_path
