import cv2
import numpy as np


import gcode_test as GC

# TODO: test using np.where

# returns a list of "points" for each position
# every point travels up, to the point, and then down
def raster_image(image):

    pos_list = []

    for row in range(image.shape[0]):
        for col in range(image.shape[1]):
            if(image[row,col] > 0):

                pos_list.append({"Z": 10})
                pos_list.append({
                                    "X": col,
                                    "Y": row
                                    })
                pos_list.append({"Z": 0})

    return pos_list


# get the contours
def test_contours(image):

    contours, heirachy = cv2.findContours(image, None, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    print(contours)

    return contours





def main():
    file = "test.png"

    image = cv2.imread(file, 0)

    pos_list = raster_image(image)

    gcode = GC.pos_list_gcode(pos_list)

    text_file = open("test.gcode", 'w')
    text_file.write(gcode)
    text_file.close()

if __name__ =="__main__":
    main()
