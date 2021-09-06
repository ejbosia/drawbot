import pytest
import os
import numpy as np
import cv2

from src.utilities.shapely_conversion import convert

from shapely.affinity import rotate

from src.fill_strategy.zigzag import ZigZag, ZigZagGenerator

'''
Test valid spiral generation using different angles of the image
'''
def test_generation():

    image = cv2.imread(os.path.join('test_images', 'test.png'), 0)

    polygons = convert(image)
    generator = ZigZagGenerator(polygons, 5)

    for i in range(180):
        generator.angle = np.radians(i)

        output = generator.generate()

        assert len(output) >= 3
        
        for zigzag in output:
            assert isinstance(zigzag, ZigZag)