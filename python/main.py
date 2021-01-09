import contour_fill as CF
import gradient_fill as GF
import cv2
import numpy as np
import argparse


# remove single_thickness_lines
def remove_single_thickness_lines(image):

    image = cv2.erode(image, np.ones((3,3)))
    image = cv2.dilate(image, np.ones((3,3)))
    return image


def main(file="picture.png", inverse=False, resize = 1):
    print(file)

    image = cv2.imread(file, 0)

    image = cv2.resize(image, None, fx=resize, fy=resize, interpolation=cv2.INTER_NEAREST)
    image = remove_single_thickness_lines(image)
    if inverse:
        image = 255-image

    CF.execute(image)


if __name__ == "__main__":
    main()