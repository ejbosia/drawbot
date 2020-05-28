import numpy as np

# takes in a position (XYZF)
# returns the gcode to enact that position
def pos_gcode(pos):

    gcode = "\bG01 "

    for key in pos.keys():
        gcode += key+str(pos[key])+" "

    gcode += ";"

    return gcode



def main():
    print("This is a test")

if __name__ == "__main__":
    main()
