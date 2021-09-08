'''
This is a cli for path generation
'''

import argparse
import warnings
import os
import cv2

from matplotlib import pyplot

# import utility functions
from src.utilities.shapely_conversion import convert

# import spiral generation
from src.fill_strategy.zigzag import ZigZagGenerator
from src.fill_strategy.spiral import SpiralGenerator, Spiral
from src.fill_strategy.outline import OutlineGenerator
from src.fill_strategy.fermat_spiral import FermatSpiralGenerator

# add-on modules
from src.utilities.metrics import Metrics
from src.utilities.gcode import GcodeWriter

parser = argparse.ArgumentParser()

parser.add_argument("filename", help="path to image file", type=str)
parser.add_argument("distance", help="line thickness", type=float)

group = parser.add_mutually_exclusive_group()
group.add_argument("-z","--zigzag", help="zigzag (rectilinear) fill", action='store_true')
group.add_argument("-s","--spiral", help="spiral fill", action='store_true')
group.add_argument("-o","--outline", help="outline fill", action='store_true')
group.add_argument("-f","--fermat", help="fermat fill", action='store_true')

parser.add_argument("-p", "--plot", help="enable plotting", action='store_true')
parser.add_argument("-g", "--gcode", help="enable output", type=str)
parser.add_argument("-m", "--metrics", help="enable metrics", action='store_true')



def plot_path(path, color=None):
    '''
    Plot a single path
    '''
    
    X = []
    Y = []

    for p in path:
        X.append(p[0])
        Y.append(p[1])
        
    pyplot.plot(X,Y,c=color)


def plot_recursive_path(total_path, color=None):
    '''
    Plot a list of fill_patterns
    '''

    for path in total_path:
        plot_path(path.get_path(), color)

        if isinstance(path, Spiral):
            for contour in path.contours:

                start = contour.coords[0]
                end = contour.coords[-1]

                pyplot.scatter(start[0],start[1])
                pyplot.scatter(end[0],end[1])

    pyplot.gca().invert_yaxis()


def main():
    
    warnings.warn("Only rectilinear fill and spiral fill is completed")

    args = parser.parse_args()

    filename = args.filename
    distance = args.distance

    assert distance > 0

    # read the image
    image = cv2.imread(filename,0)
    assert not image is None
    
    polygons = convert(image, approximation = cv2.CHAIN_APPROX_SIMPLE, simplify=1)

    path_type = ""

    # determine which path to create
    if args.zigzag:
        results = ZigZagGenerator(polygons, distance).generate()
        path_type = "ZZ"
    elif args.spiral:
        results = SpiralGenerator(polygons, distance).generate()
        path_type = "S"
    elif args.outline:
        results = OutlineGenerator(polygons).generate()
        path_type = "O"
    elif args.fermat:
        results = FermatSpiralGenerator(polygons, distance).generate()
        path_type = "F"
    else:
        raise NotImplementedError("FILL TYPE NOT INPUT")

    if args.plot:
        plot_recursive_path(results)
        pyplot.show()
    
    if not args.gcode is None:
        assert args.gcode.split('.')[-1] == 'gcode'
        gcode_writer = GcodeWriter(filename=args.gcode, scale = 0.1)
        gcode_writer.convert(results)
    
    if args.metrics:
        metric = Metrics(segments=True, commands=True, curvature=False, underfill=True, overfill=True)
        print(metric.measure(results, os.path.basename(filename), path_type, distance, polygons))


if __name__ == "__main__":
    main()