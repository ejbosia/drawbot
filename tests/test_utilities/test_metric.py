
from utilities.metrics import Metrics

from fill_strategy.zigzag import ZigZagGenerator
from fill_strategy.spiral import SpiralGenerator

from utilities.shapely_conversion import convert

import numpy as np
import cv2
import os
import pytest

'''
Test number of commands is correctly calculated
'''
def test_commands():

    metric = Metrics()
    image = cv2.imread(os.path.join('test_images', 'test.png'),0)
    polygons = convert(image)

    generator = ZigZagGenerator(polygons, 5)
    output = generator.generate()

    assert metric.measure_commands(output) == sum([len(x.get_path()) for x in output])
    
    generator = SpiralGenerator(polygons, 5)
    output = generator.generate()

    assert metric.measure_commands(output) == sum([len(x.get_path()) for x in output])


def test_curvature():
    pass

def test_overfill():
    pass

def test_underfill():
    pass