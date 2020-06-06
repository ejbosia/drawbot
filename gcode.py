import numpy as np
import matplotlib.pyplot as plt
import config as CONFIG
# takes in a position (XYZF)
# returns the gcode to enact that position
def pos_gcode(pos):

    gcode = "G01 "

    for key in pos.keys():
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
# input gcode which is \n separated, output a line plot
# this is assuming all commands are XY, or Z
def plot_gcode(gcode, debug=True):
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
        plt.plot(X[i], Y[i])

    Z_down = np.array(Z_down).transpose()
    Z_up = np.array(Z_up).transpose()
    if debug:
        print(Z_down)
    plt.scatter(x=Z_down[0], y=Z_down[1], c="blue", s=5)
    plt.scatter(x=Z_up[0], y=Z_up[1], c='red', s=3)
    #plt.gca().invert_yaxis()
    plt.show()

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
