import numpy as np
import matplotlib.pyplot as plt
import config as CONFIG


# takes in a position (XYZF)
# returns the gcode to enact that position
def pos_gcode(pos, no_scale=False):

    gcode = "G01 "

    for key in pos.keys():
        if no_scale:
            gcode += key+str(pos[key])+" "

        else:
            gcode += key+str(pos[key] * CONFIG.SCALE)+" "

    gcode += ";\n"

    return gcode


# iterate through a list of positions to generate gcode
def pos_list_gcode(pos_list):

    gcode = ""

    for pos in pos_list:
        gcode += pos_gcode(pos)

    return gcode


# assuming XYZF order
# convert array to dict format
def format_pos(pos):

    axis = ["X","Y","Z","F"]
    format_pos = {}
    for i,value in enumerate(pos):
        format_pos[axis[i]] = value

    return format_pos


# get the next avaiable partition
# start looking to the right of the partition, clockwise search
def next_paritition(pt, points, direction):

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

    # do one full loop if no partitions are found
    for i in range(8):

        check_pt = pt + check[(direction+i)%8]

        mask = ((check_pt == points).all(axis=1))

        if(mask.any()):
            return points[mask][0], (direction+i)%8

    return np.array([]), direction


# returns the spiral fill of gcode
def chain_spiral(chain, debug=True):
    sort_chain = np.array(chain)
    # sort the partitions (first is top left, sorts row before column)
    sort_chain = sort_chain[sort_chain[:,0].argsort()]

    # take the first partition out of the list
    pt = sort_chain[0]
    sort_chain = np.delete(sort_chain, 0, axis=0)
    gcode = "\nG01 Z5;\n"
    gcode += pos_gcode(format_pos(pt))

    direction = 0

    pen_up = True

    while sort_chain.size > 0:
        new_pt, dir = next_paritition(pt, sort_chain, direction)

        if pen_up:
            gcode += pos_gcode(format_pos(pt))
            gcode += "G01 Z0;\n"
            pen_up = False

        # if there are no new points, add the last point as gcode
        if new_pt.size == 0:
            if debug:
                print("Option: 0\t", direction, "\t", dir, "\t", pt)
            gcode += pos_gcode(format_pos(pt))
            gcode += "G01 Z5;\n"
            pen_up = True
            pt = sort_chain[0]
            direction = 0
        # if the direction changes, add the last point as gcode
        elif dir != direction:
            if debug:
                print("Option: 1\t", direction, "\t", dir, "\t", pt)
            gcode += pos_gcode(format_pos(pt))
            pt = new_pt
            direction = dir
        # if the direction does not change, no need to add the last point as gcode
        else:
            if debug:
                print("Option: 2\t", direction, "\t", dir, "\t", pt)
            pt = new_pt


        # remove the current point from the sort chain
        sort_chain = sort_chain[(pt != sort_chain).any(axis=1)]

    gcode += pos_gcode(format_pos(pt))
    gcode += "G01 Z5;\n"

    return gcode


def chain_contour(chain):

    first_point = True

    gcode = ""
    for pt in chain:
        gcode += pos_gcode(format_pos(pt))

        if first_point:
            gcode += "G01 Z0;\n"
            first_point = False

    gcode += "G01 Z5;\n"
    return gcode


#fill the chain with back and forth horizontal lines
# hopefully minimizes the pen up and down motions
def line_fill(chain):
    direction_neg = True

    gcode = ""

    previous = np.array([-2,-2])

    for i in range(chain[:,1].min(), chain[:,1].max()+1):
        temp = chain[chain[:,1]==i]
        #print(temp)

        sort_temp = temp[temp[:,0].argsort()]

        if direction_neg:
            sort_temp = sort_temp[::-1]

        if abs(sort_temp[0][0]-previous[0]) <= 1:
            gcode += pos_gcode(format_pos(sort_temp[0]))
            #print(sort_temp[0][0], previous[0], "FOO")

        #else:
            #print(sort_temp[0][0], previous[0])


        for pt in sort_temp:

            if abs(pt[0]-previous[0]) > 1:
                gcode += pos_gcode(format_pos(previous))
                gcode += "G01 Z10;\n"
                gcode += pos_gcode(format_pos(pt))
                gcode += "G01 Z0;\n"
            previous = pt

        # the final command in the list should move to a position and raise the pen
        gcode += pos_gcode(format_pos(pt))
        # gcode += "G01 Z10;\n"

        direction_neg = not direction_neg

    # raise pen at the end of the chain
    gcode += "G01 Z10;\n"
    return gcode


#fill the chain with back and forth horizontal lines
# hopefully minimizes the pen up and down motions - OPTIMIZED
def line_fill_2(chain):
    direction = True

    gcode = "G01 Z10;\n"

    # sort chain by row
    chain = chain[chain[:,0].argsort()]

    # create a temporary line of points
    index = chain[:,1].min()
    temp = chain[chain[:,1]==index]
    sort_temp = temp[temp[:,0].argsort()]
    pt = sort_temp[0]
    gcode += pos_gcode(format_pos(pt))
    gcode+= "G01 Z0;\n"



    # loop while points exist in the chains
    while(chain.size > 0):

        next_pt = pt + np.array([1,0])

        # set the direction
        direction = not (next_pt == chain).all(axis=1).any()
        temp = chain[np.where(chain[:,1] == pt[1])]
        print(temp.size, pt, temp)
        #print(chain.size)
        # loop until the end of the chain breaks the loop
        #print(sort_temp[(sort_temp != pt).any(axis=1)])
        temp_chain = []
        start_pt = pt


        while True:
            # remove the point from the chain
            temp_chain.append(pt)
            #print(pt)
            if direction:
                next_pt = pt + np.array([1,0])
            else:
                next_pt = pt + np.array([-1,0])
            # print(pt)
            # print(next_point,'\t',(next_point == sort_temp).all(axis=1))
            # if the next point does not exist, break the loop
            #print(next_pt, next_pt==temp, temp)
            if (next_pt == temp).all(axis=1).any():
                pt = next_pt
                print("A")
            else:
                gcode += pos_gcode(format_pos(pt))
                print("B")
                break
        # print("NEW ROW", pt)
        temp_chain = np.array(temp_chain)
        dims = np.maximum(temp_chain.max(0),chain.max(0))+1
        chain = chain[~np.in1d(np.ravel_multi_index(chain.T,dims),np.ravel_multi_index(temp_chain.T,dims))]

        if chain.size == 0:
            break

        try:
            # find the next point
            pt = next_point_lf(pt, start_pt,chain, direction)
            gcode += pos_gcode(format_pos(pt))
            chain = chain[(chain!=pt).any(axis=1)]
            #print(pt)
        # if no point is found, pick the highest point
        except ValueError:
            gcode += "GO1 Z10;\n"
            # print("VALUE ERROR")
            index = chain[:,1].min()
            temp = chain[chain[:,1]==index]
            sort_temp = temp[temp[:,0].argsort()]
            pt = sort_temp[0]

            chain = chain[(chain!=pt).any(axis=1)]
            gcode += pos_gcode(format_pos(pt))
            gcode += "GO1 Z0;"

    gcode += "G01 Z10;\n"
    return gcode

#fill the chain with back and forth horizontal lines
# hopefully minimizes the pen up and down motions - OPTIMIZED
def line_fill_3(chain, contour):
    direction_neg = True

    gcode = "G01 Z10;\n"

    # sort chain by row
    previous = np.array([-2,-2])
    contour = np.array(contour)

    # create a temporary line of points
    index = chain[:,1].min()
    temp = chain[chain[:,1]==index]
    sort_temp = temp[temp[:,0].argsort()]
    pt = sort_temp[0]


    gcode += pos_gcode(format_pos(pt))
    gcode+= "G01 Z0;\n"
    prev_direction = True

    # loop while points exist in the chains
    while(chain.size > 0):
        #print(chain.size)
        # loop until the end of the chain breaks the loop
        #print(sort_temp[(sort_temp != pt).any(axis=1)])

        temp_chain = []

        while True:


            # remove the point from the chain
            # remove the point from the contour
            temp_chain.append(pt)

            left_pt = pt + np.array([-1,0])
            right_pt = pt + np.array([1,0])

            #print(next_point,'\t',(next_point == sort_temp).all(axis=1))
            # if the next point does not exist, break the loop
            if (left_pt == chain).all(axis=1).any():
                pt = left_pt
            elif (right_pt == chain).all(axis=1).any():
                pt = right_pt
            else:
                gcode += pos_gcode(format_pos(pt))
                break
        temp_chain = np.array(temp_chain)
        #print(temp_chain)

        chain = chain[(chain!=temp_chain).any(axis=1)]

        if chain.size == 0:
            break

        direction_neg  = not direction_neg
        try:
            # find the next point
            pt = next_point_contour(pt,chain, contour)
            gcode += pos_gcode(format_pos(pt))
            chain = chain[(chain!=pt).any(axis=1)]
            contour = contour[(contour!=pt).any(axis=1)]

        # if no point is found, pick the highest point
        except ValueError:
            # print("VALUE ERROR")
            gcode += "GO1 Z10;\n"
            pt = chain[0]
            chain = chain[(chain!=pt).any(axis=1)]
            contour = contour[(contour!=pt).any(axis=1)]
            gcode += pos_gcode(format_pos(pt))
            gcode += "GO1 Z0;"

    gcode += "G01 Z10;\n"
    return gcode

# next point contour function
def next_point(p, temp, i):
    y = p["Y"]

    # print(temp.head())
    index = temp.index.get_loc(p.name[1])
    # print(index)

    next_pt = temp.iloc[(index + 1) % temp.shape[0]]
    prev_pt = temp.iloc[index - 1]
    # print(i, index)

    if next_pt["Available"] and next_pt["Y"] - y == 1:
        next_pt.name = (i, next_pt.name)
        return next_pt
    elif prev_pt["Available"] and prev_pt["Y"] - y == 1:
        prev_pt.name = (i, prev_pt.name)
        return prev_pt
    else:
        raise ValueError




def next_point_contour(pt,points,contour):
        #print("NP")
        #print(pt, contour[contour[:,1]==pt[1]])

        index = np.where((contour==pt).all(axis=1))[0]
        #print(pt, contour)

        if not index:
            raise ValueError

        index = index[0]
        #print(index, contour.size, contour.shape[0])
        if index+1 == contour.shape[0]:
            check_pt = contour[0]
        else:
            check_pt = contour[index+1]


        #print("NPC",index,pt,check_pt,contour[index-1], contour.size)

        #print(check_pt, points, (check_pt == points))

        # check one direction
        if ((check_pt == points).all(axis=1)).any():
            #print(check_pt,direction_neg,c,pt)
            return check_pt

        # check the other direction
        check_pt = contour[index-1]


        if ((check_pt == points).all(axis=1)).any():
            #print(check_pt,direction_neg,c,pt)
            return check_pt

        raise ValueError

def next_point_lf(pt,start_pt, points, direction):
        #direction = not direction
        #Sprint("NEXT FUNC",pt)
        x_min = points.min(axis=0)[0]
        x_max = points.max(axis=0)[0]

        # if there are any points remaining above
        check_x = points[np.where(points[:,1] == pt[1]+1)].transpose()[0]
        row = pt[1]+1
        # if there are no points

        '''
        if check_x.size == 0:
            #print("DOWN")
            check_x = points[np.where(points[:,1] == pt[1]-1)].transpose()[0]

            row = pt[1]-1
        '''
        # if there are still no points
        if check_x.size == 0:
            # print("NO POINTS")
            #print("NO POINTS")
            raise ValueError

        start_value = pt[0] in check_x
        value = False

        # if the start value is positive, there is no limit
        if start_value:
            if direction:
                #print("NEGATIVE", direction, start_value)
                #print(check_x)

                for x in range(pt[0], x_max, 1):
                    value = x in check_x
                    #print(start_value, value, x)

                    # if the value is positive, set the index
                    if value:
                        index = x

                    # if the value is different
                    if value != start_value:
                        #print("FOUND NEG")
                        return np.array([index, row])
            else:
                #print("POSITIVE", direction, start_value)
                #print(check_x)
                #print(pt)
                for x in range(pt[0], x_min, -1):
                    value = x in check_x
                    #print(start_value, value, x)
                    # if the value is positive, set the index
                    if value:
                        index = x

                    # if the value is different
                    if value != start_value:
                        #print("FOUND POS")
                        return np.array([index, row])

        # if the start value is false, set the limits to be between start_pt and pt
        else:

            x_min = np.array([pt[0],start_pt[0]]).min()
            x_max = np.array([pt[0],start_pt[0]]).max()
            '''
            x_min = pt[0]-6
            x_max = pt[0]+6
            '''
            #print("POS", x_min, x_max, pt, start_pt)
            if direction:
                #print(check_x)
                for x in range(pt[0], x_min-1, -1):
                    value = x in check_x
                    #print(start_value, value, x)
                    # if the value is positive, set the index
                    if value:
                        index = x

                    # if the value is different
                    if value != start_value:
                        #print("FOUND POS")
                        return np.array([index, row])
            else:
                #print("NEGATIVE", direction, start_value)
                #print(check_x)
                for x in range(pt[0], x_max+1, 1):
                    value = x in check_x

                    # if the value is positive, set the index
                    if value:
                        index = x

                    # if the value is different
                    if value != start_value:
                        #print("FOUND NEG")
                        return np.array([index, row])


        if value:
            return np.array([index, row])

        raise ValueError

# fill using the contours
def line_fill_contours(contours, heirachy):

    # loop through the contours
    for x, contours in enumerate(contours):
        print("FOO")


# input gcode which is \n separated, output a line plot
# this is assuming all commands are XY, or Z
def plot_gcode(gcode, debug=True, show=True, image=False, startstop = True):
    commands = gcode.split('\n')

    X = [[]]
    Y = [[]]
    Z_down = []
    Z_up = []

    pen_down = False
    prev_x = 0
    prev_y = 0


    for c in commands:
        if debug:
            print(c)
        if "Z0" in c:
            Z_down.append(np.array([prev_x, prev_y]))
            X.append([prev_x])
            Y.append([prev_y])
            pen_down=True
        if ("X" in c or "Y" in c):
            if pen_down:
                X[-1].append(float(c.split("X")[1].split(" ")[0]))
                Y[-1].append(float(c.split("Y")[1].split(" ")[0]))
            prev_x = float(c.split("X")[1].split(" ")[0])
            prev_y = float(c.split("Y")[1].split(" ")[0])

        if not "Z0" in c and "Z" in c:
            try:
                pen_down=False
                Z_up.append(np.array([prev_x, prev_y]))
            except IndexError:
                continue
        if c == "" and debug:
            print("HAHAHA")
    for i, temp in enumerate(X):
        plt.plot(X[i], Y[i], linewidth=0.2)

    Z_down = np.array(Z_down).transpose()
    Z_up = np.array(Z_up).transpose()




    if debug:
        print(Z_down)

    if startstop:
        plt.scatter(x=Z_down[0], y=Z_down[1], c="blue", s=50)
        plt.scatter(x=Z_up[0], y=Z_up[1], c='red', s=10)
    #plt.ylim(25)
    #plt.gca().invert_yaxis()
    try:
        plt.imshow(image.transpose(),'gray')
    except:
        print("No Image")
    if show:
        plt.show()

    print("DOWN:\t", Z_down.shape)
    print("UP:\t", Z_up.shape)
def main():

    test_pos = {
                "X":100,
                "Y":100,
                "F":1000
                }

    test_z = {
                "Z": 10
                }


    print(pos_gcode(test_pos))
    print(pos_gcode(test_z))

if __name__ == "__main__":
    main()
