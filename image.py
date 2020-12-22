import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import interactive
import datetime
import gcode as GC
import pandas as pd
import math


import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)



from geometry.line import Line
from geometry.contour import Contour


# returns a list of "points" for each position
# every point travels up, to the point, and then down
def raster_image(image):

    pos_list = []

    for row in range(image.shape[0]):
        for col in range(image.shape[1]):
            if image[row, col] > 0:

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


# remove unnecessary points from a list of dataframes
def clean_points(g_list):
    gradient_list = []
    for gtest in g_list:
        gradient = gtest[(gtest["Y-"] != gtest["Y+"])]

        gradient = gradient[(gradient["Y+"] == gradient["Y"]+1)|
                            (gradient["Y-"] == gradient["Y"]+1)]

        gradient_list.append(gradient)
    return gradient_list


def create_super_list(contours):
    super_list = []

    for c in contours:
        data_list = contour_to_dataframe(c)
        super_list.append(data_list)

    return list(map(clean_points, super_list))

'''
Run the old method of contours
'''
def old_method(image):
    chain_list, contours = contour_groups(image)

    start = datetime.datetime.now()
    super_list = create_super_list(contours)

    # gcode += GC.chain_contour(contour_list)
    gcode = GC.process_contours(super_list)

    print("Total time:", datetime.datetime.now()-start)

    GC.plot_gcode(gcode, debug=False, image=image, scale=False)

    text_file = open("test.gcode", 'w')
    text_file.write(gcode)
    text_file.close()


def ravel_lines(line_list):

    X = []
    Y = []

    for line in line_list:
        if not X and not Y:
            X.append(line.p1[0])
            Y.append(line.p1[1])

        X.append(line.p2[0])
        Y.append(line.p2[1])
    
    return X, Y

def plot_contours(contour_list, show=True, points=True):

    for contour in contour_list:

        X,Y = ravel_lines(contour.line_list)
        plt.plot(X,Y)

        if points:
            for x,y in zip(X,Y):
                plt.scatter(x,y)
    
    if show:
        plt.show()


# create border lines for the image
# return a list of lists of lines
def generate_border_lines(image):

    contours,heirarchy = cv2.findContours(image, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)  

    contour_list = []

    for contour,heirarchy in zip(contours, heirarchy[0]):
        line_list = []
        pt0 = None
        for c in contour:
            # if this is the first point do not create a line
            if not pt0 is None:
                line_list.append(Line(pt0, p2=tuple(c[0])))
            
            pt0 = tuple(c[0])

        # add the last line from the last first point to the starting point
        line_list.append(Line(pt0, p2 = tuple(contour[0][0])))

        contour_list.append(Contour(line_list, heirarchy))

    return contour_list


# fill contours towards other edge
# hole contours away from other edge
def fill_direction(contour, point, angle):

    # force the angle within 0-2PI
    angle = angle % (2*np.pi)

    # find the direction that is "inside" the contour
    ray = Line(point, angle = angle)
    
    # if there is no intersection, the direction must be the opposite for "fill" contours
    if not contour.intersection(ray) and contour.heirarchy[3] == -1:
        angle = angle - math.pi
    # if there is an intersection, the direction must be the opposite for "hole" contours
    elif contour.intersection(ray) and not contour.heirarchy[3] == -1:
        angle = angle - math.pi


    # if this is a "fill" contour, return the angle of intersection
    if contour.heirarchy[3] == -1:
        return angle
    # if this is a "hole" contour, return the angle away from intersection
    else:
        return angle - math.pi


# find the closest intersection from the ray - returns the contour and the point
def find_closest_intersection(contour_list, ray):

    possible_contours = []

    # find all contours that intersect (fast)
    for contour in contour_list:
        if contour.fast_intersection(ray):
            possible_contours.append(contour)

    points = []
    contours = []

    # find all intersection points
    for contour in possible_contours:

        point = contour.intersection(ray)
        if not point is None:
            points.extend(point)

            # add a contour for each point
            for _ in range(len(point)):
                contours.append(contour)

    # find the closest point
    length = Line(ray.p1, p2 = points[0]).length()
    closest_point = points[0]
    closest_contour = contours[0]

    for contour, point in zip(contours,points):
        new_length = Line(ray.p1, p2 = point).length()
        if length > new_length:
            length = new_length
            closest_point = point
            closest_contour = contour

    return closest_contour, closest_point



def fill_contours(contour_list, line_thickness=1, angle=math.pi/6):


    # start at contour 0
    previous_contour = contour_list[1]

    contour = previous_contour
    # pick a point
    new_point = contour.line_list[0].bisect()

    traverse_amount = -line_thickness

    line_x = [new_point[0]]
    line_y = [new_point[1]]

    for i in range(10):
        # determine a direction
        angle = fill_direction(contour, new_point, angle)
        ray = Line(new_point, angle=angle)

        contour, point = find_closest_intersection(contour_list, ray)

        ray.p2 = point

        line_x.append(point[0])
        line_y.append(point[1])

        plot_contours(contour_list,show=False,points=False)
        
        plt.plot(line_x, line_y)

        # traverse
        
        # if(contour == previous_contour):
        #     traverse_amount = -traverse_amount

        # new_point = contour.traverse(point, traverse_amount)

        # build the new line

        dy, dx = ray.slope()

        temp = Line(c)


        line_x.append(new_point[0])
        line_y.append(new_point[1])

        print("COMPLETE", i)

    plt.show()


def main(file="test_ring.png", inverse=False, resize = 1):
    print(file)

    image = cv2.imread(file, 0)

    image = cv2.resize(image, None, fx=resize, fy=resize, interpolation=cv2.INTER_NEAREST)

    if inverse:
        image = 255-image

    contours = generate_border_lines(image)

    fill_contours(contours)

if __name__ == "__main__":
    main()
