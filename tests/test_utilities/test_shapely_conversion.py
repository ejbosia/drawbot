'''
Test different shapely conversions
'''

import src.utilities.shapely_conversion as SC

import os
import cv2

from shapely.geometry import Polygon

import pytest

def test_generate_border_lines():

    # get the square boundaries    
    square = cv2.imread(os.path.join('test_images', 'test.png'), 0)

    # get the border lines
    borders = SC.generate_border_lines(square)

    assert len(borders) == 5

def test_create_contour_families():

    # get multiple boundaries
    test = cv2.imread(os.path.join('test_images', 'test.png'), 0)

    # get the border lines (should be 5 total, each with 4 sides)
    borders = SC.generate_border_lines(test)
    
    assert len(borders) == 5

    # get the polygons
    polygons = SC.create_contour_families(borders)

    assert len(polygons) == 3

    interiors = 0
    # only one polygon should have a hole
    for p in polygons:
        interiors += len(p.interiors)

    assert interiors == 2


def test_convert():

    # test bad simplify value
    with pytest.raises(ValueError) as error:
        SC.convert(None, simplify=-1)

    assert error.value.args[0] == "SIMPLIFY MUST BE GEQ 0"
    assert error.type == ValueError

    image = cv2.imread(os.path.join('test_images', 'test.png'),0)
    polygons1 = SC.convert(image)
    polygons2 = SC.convert(image, simplify=1)

    for p1, p2 in zip(polygons1, polygons2):
        assert len(p1.exterior.coords) >= len(p2.exterior.coords)
        assert abs(p1.area - p2.area) < 0.01*p1.area