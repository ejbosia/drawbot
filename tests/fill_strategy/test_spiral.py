import os
import numpy as np
import cv2

from utilities.shapely_conversion import convert

from fill_strategy.spiral import Spiral, SpiralGenerator


def test_generation():
    '''
    Test valid spiral generation using different angles of the image
    '''
    image = cv2.imread(os.path.join('test_images', 'test.png'), 0)

    polygons = convert(image)

    generator = SpiralGenerator(polygons, 5)

    for i in range(0, 91, 30):
        generator.angle = np.radians(i)

        output = generator.generate()

        assert len(output) >= 3

        for spiral in output:
            assert isinstance(spiral, Spiral)
