import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

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
    gcode += "F12000 "
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

    axis = ["X", "Y", "Z", "F"]

    format_pos = {}
    for i,value in enumerate(pos):
        format_pos[axis[i]] = value

    return format_pos


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


# fill the contour
def contour_fill(data):
    if data.empty:
        return ""

    test = data.copy()

    p = test.iloc[0]

    gcode = "G01 Z10;\n"
    gcode += pos_gcode(format_pos([p["X"], p["Y"]]), no_scale=False)
    gcode += "G01 Z0;\n"

    while test["Available"].any():

        try:
            test.at[p.name, "Available"] = False
            row = test[test["Y"] == p["Y"]]

            gcode += pos_gcode(format_pos([p["X"], p["Y"]]), no_scale=False)

            xp = row[row["X"] > p["X"]].sort_values("X")
            xm = row[row["X"] < p["X"]].sort_values("X", ascending=False)
            pminus = pd.DataFrame()
            pplus = pd.DataFrame()

            if not xp[xp["Available"]].empty:
                pplus = xp[xp["Available"]].iloc[0]
            if not xm[xm["Available"]].empty:
                pminus = xm[xm["Available"]].iloc[0]

            # determine the direction
            # any contours, except the outer contour, cannot travel to themselves
            # outer contour only goes towards odd direction - even direction is closed contours
            if p.name[0] == 0:
                if (not pminus.empty) and xm.shape[0] % 2 == 1:
                    p2 = pminus
                elif (not pplus.empty) and xp.shape[0] % 2 == 1:
                    p2 = pplus
                else:
                    raise ValueError
            else:
                if not pminus.empty and xm.shape[0] % 2 == 1:
                    p2 = pminus
                elif not pplus.empty and xp.shape[0] % 2 == 1:
                    p2 = pplus
                else:
                    raise ValueError

            test.at[p2.name, "Available"] = False

            gcode += pos_gcode(format_pos([p2["X"], p2["Y"]]), no_scale=False)

            p = next_point(p2, test.loc[p2.name[0]], p2.name[0])

        except ValueError as e:

            gcode += "G01 Z10;\n"

            if not test["Available"].any():
                break

            p = test[test["Available"]].sort_values(["Y", "X"]).iloc[0]

            gcode += pos_gcode(format_pos([p["X"], p["Y"]]), no_scale=False)

            gcode += "G01 Z0;\n"

            direction = True

    return gcode


# process all of the contours from an image
def process_contours(super_list):
    gcode = ""

    for x, data_list in enumerate(super_list):

        print(round(x * 100 / len(super_list), 2), "%")

        # build the dataframe
        temp = pd.DataFrame()

        for data in data_list:
            temp = temp.append(data)
        temp = temp.reset_index()
        temp = temp.set_index(["FRAME", "index"])

        # print(temp.head())
        gcode += contour_fill(temp)

    return gcode


# input gcode which is \n separated, output a line plot
# this is assuming all commands are XY, or Z
def plot_gcode(gcode, debug=True, show=True, image=False, startstop=True, scale=True):
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
        if "X" in c or "Y" in c:
            if pen_down:
                if scale:
                    X[-1].append(float(c.split("X")[1].split(" ")[0]))
                    Y[-1].append(float(c.split("Y")[1].split(" ")[0]))
                else:
                    X[-1].append(float(c.split("X")[1].split(" ")[0]) / CONFIG.SCALE)
                    Y[-1].append(float(c.split("Y")[1].split(" ")[0]) / CONFIG.SCALE)
            if scale:
                prev_x = float(c.split("X")[1].split(" ")[0])
                prev_y = float(c.split("Y")[1].split(" ")[0])
            else:
                prev_x = float(c.split("X")[1].split(" ")[0]) / CONFIG.SCALE
                prev_y = float(c.split("Y")[1].split(" ")[0]) / CONFIG.SCALE

        if not ("Z0" in c) and "Z" in c:
            try:
                pen_down = False
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
