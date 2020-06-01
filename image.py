import cv2
import numpy as np
import matplotlib.pyplot as plt

import gcode as GC

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


# get available points
# available points are all of the points around the point
def get_available_pts(pt, points):
    available_pts = []

    # array of the different directions around the points
    # these values are added to the test point to create the check points
    check = np.array([
        [0,1],
        [1,1],
        [1,0],
        [1,-1],
        [0,-1],
        [-1,-1],
        [-1,0],
        [-1,1]
    ])

    for c in check:
        check_pt = pt + c

        mask = ((check_pt == points).all(axis=1))

        if(mask.any()):
            available_pts.append(points[mask][0])



    return available_pts

# recursively get combine points into chains
def get_chain(pt, points):

    chain = []
    available_pts = get_available_pts(pt, points)

    # remove the available pts --> they have already been checked
    for p in available_pts:
        points = points[(p != points).any(axis=1)]
    # print(pt, "\t", available_pts)
    if available_pts:
        for avp in available_pts:
            # recursivly check the new points
            chain.append(avp)
            chain.extend(get_chain(avp, points))
        return chain

    else:
        return []

# plot the points in a chain individually
def plot_points(point_chain):
    for chain in point_chain:
        format = np.array(chain).transpose()
        row = format[0]
        col = format[1]
        plt.scatter(x=col, y=row)

    plt.gca().invert_yaxis()
    plt.show()


# converts an image into motion vectors
def vector_test(image):

    # raise NotImplementedError

    # find the black pixels
    points = np.array(np.where(image==0)).transpose()

    point_chain = []

    # find chains of pixels while there are pixels left
    while(points.size > 0):
        # pick the first points
        pt = points[0]
        points = points[(pt != points).any(axis=1)]

        temp = [pt]
        temp.extend(get_chain(pt, points))
        point_chain.append(temp)
        print(temp)
        # remove the points already checked
        for p in temp:
            points = points[(p != points).any(axis=1)]

        print(points.size)


    return point_chain

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
