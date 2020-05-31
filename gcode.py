import numpy as np

# takes in a position (XYZF)
# returns the gcode to enact that position
def pos_gcode(pos):

    gcode = "G01 "

    for key in pos.keys():
        gcode += key+str(pos[key])+" "

    gcode += ";\n"

    return gcode


# iterate through a list of positions to generate gcode
def pos_list_gcode(pos_list):

    gcode = ""

    for pos in pos_list:
        gcode += pos_gcode(pos)

    return gcode

# get the next avaiable partition
# start looking to the right of the partition, clockwise search
def next_paritition(pt, points):

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
            return points[mask][0]

    return available_pts



# returns the spiral fill of gcode
def chain_spiral(chain):
    gcode = ""

    # sort the partitions (first is top left, sorts row before column)
    sort_chain = np.array(chain).sort(axis=0)

    # take the first partition out of the list
    pt = sort_chain[0]
    sort_chain = np.delete(sort_chain, 0, axis=0)

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

    direction = 0

    while sort_chain.size > 0:

        check_pt = pt + check[direction]

        mask = ((check_pt == points).all(axis=1))
        # if a point exists in the direction
        if(mask.any()):
            pt = check_pt
            sort_chain = sort_chain[(pt != sort_chain).any(axis=1)]
        # if the search direction is past
        elif direction > 7:
            pt = sort_chain[0]
            sort_chain = np.delete(sort_chain, 0, axis=0)
        else:
            pos_gcode(pt)
    return gcode


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
