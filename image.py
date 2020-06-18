import cv2
import numpy as np
import matplotlib.pyplot as plt
import datetime
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


# get the contour groups using hierarchy
def contour_groups(image):

    chain_list = []
    contour_list = []

    # find the contours and the hierarchy
    # cv2.RETR_CCOMP returns the filled areas and holes (hierarchy is only two levels)
    contours,hierarchy = cv2.findContours(image, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)

    # loop through the contours and the hierarchy
    for c,h in zip(contours, hierarchy[0]):

        # only fill in if there are no parents
        if h[3] == -1:
            mask = cv2.drawContours(np.zeros_like(image), [c], 0, 255, -1)
            contour_list.append([])
            contour_list[-1].append(get_contour_points(c))
            print(len(contour_list[-1][0]))
            next_contour = h[2]

            while(next_contour != -1):
                # remove this area from the contour
                mask = cv2.drawContours(mask, contours, next_contour, 0, -1)

                # fill in inner edge
                mask = cv2.drawContours(mask, contours, next_contour, 255, 1)

                contour_list[-1].append(get_contour_points(contours[next_contour]))
                next_contour = hierarchy[0][next_contour, 0]
                '''
                plt.imshow(mask, 'gray')
                plt.title(len(contour_list[-1]))
                plt.show()
                '''
            points = np.array(np.where(mask == 255)).transpose()
            chain_list.append(points)

    return chain_list, contour_list


def get_contour_points(contour):
    pts = []
    for c in contour:
         pts.append(c[0][::-1])

    return pts


# add the previous and next point values to the gradient data
def gradient_data(data):
    data.loc[:, "Y-"] = data["Y"].shift()
    data.loc[:, "Y+"] = data["Y"].shift(-1)

    data.iloc[0, data.columns.get_loc('Y-')] = data.iloc[-1, data.columns.get_loc('Y')]
    data.iloc[-1, data.columns.get_loc('Y+')] = data.iloc[0, data.columns.get_loc('Y')]
    data.loc[:, "dY"] = data["Y+"] - data["Y-"]

    data.loc[:, "Available"] = True

    return data


# convert a list of contours to a list of dataframes - one dataframe for each contour
def contour_to_dataframe(contours):
    c_list = []

    data_list = []

    for x, contour in enumerate(contours):
        print(x)
        for c in contour:
            c_list.append({"X": c[0], "Y": c[1]})
            c_list[-1]["FRAME"] = x

        temp = gradient_data(pd.DataFrame(c_list))
        data_list.append(temp)
        c_list = []

    return data_list


def main(file="test.png", inverse=False):
    print(file)

    image = cv2.imread(file, 0)

    if inverse:
        image = 255-image

    chain_list, contour_list = contour_groups(image)

    gcode = ""
    start = datetime.datetime.now()

    for c in chain_list:
        #print(c)
        gcode += GC.line_fill_2(c)

    print("Line Fill 2", datetime.datetime.now()-start)
    GC.plot_gcode(gcode,debug=False, image=image)

    text_file = open("test.gcode", 'w')
    text_file.write(gcode)
    text_file.close()

if __name__ =="__main__":
    main()
