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
        #print(points)
        points = points[(p != points).any(axis=1)]
    if available_pts:
        for avp in available_pts:
            # recursivly check the new points
            chain.append(avp)
            temp, points = get_chain(avp,points)
            chain.extend(temp)
        return chain, points

    else:
        return [], points

# plot the points in a chain individually
def plot_points(point_chain):
    for chain in point_chain:
        format = np.array(chain).transpose()
        row = format[0]
        col = format[1]
        plt.scatter(x=col, y=row)

    plt.legend()
    plt.gca().invert_yaxis()
    plt.show()


# get the contours
def contour_groups(image):

    contours, heirachy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    chain_list = [[]]

    for c in contours:
        mask = np.zeros_like(image)

        for pt in c:
            chain_list[-1].append(pt[0])
        chain_list[-1].append(c[0][0])
        chain_list.append([])

        x = points.size
        for cp in chain_list[-2]:
            #print(cp,points[0], points.shape)
            points = points[(cp != points).any(axis=1)]
        # print(x, points.size)
    return chain_list


def main(file = "test.png"):
    print(file)

    image = cv2.imread(file, 0)
    image = 255-image
    #chain_list = vector_test(image)
    #chain_list, point_list = contour_groups(image)
    #point_list = contour_groups_v2(image)

    p = np.array(np.where(image==255)).transpose()

    gcode = ""
    '''
    for c in chain_list:
        gcode += GC.chain_contour(c)
    '''
    '''
    for p in point_list:
        #print(p)
    '''
    gcode += GC.line_fill(p)

    GC.plot_gcode(gcode,debug=False)

    text_file = open("test.gcode", 'w')
    text_file.write(gcode)
    text_file.close()

if __name__ =="__main__":
    main()
