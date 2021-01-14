
from geometry.line import Line

import matplotlib.pyplot as plt
import numpy as np


def crossProduct(p, angle):

    s = np.sin(angle)
    c = np.cos(angle)

    x = p[0] * c - p[1] * s
    y = p[0] * s + p[1] * c

    return x,y


def rotation(p, ray):

    angle = -ray.angle

    p_new = (p[0]-ray.p1[0],p[1]-ray.p1[1])
    
    x,y = crossProduct(p_new, angle)


    return (x+ray.p1[0],y+ray.p1[1])


def checkIntersection(ray, line):

    pr1 = rotation(line.p1, ray)
    pr2 = rotation(line.p2, ray)

    print(line.p1, line.p2)
    print(pr1, pr2)
    
    Y = pr1[1] * pr2[1] < 0# signs are opposite

    if not Y:
        print("Y", Y)
        return False

    dx1 = pr1[0] - ray.p1[0]
    dy1 = pr1[1] - ray.p1[1]

    dx2 = pr2[0] - ray.p1[0]
    dy2 = pr2[1] - ray.p1[1]

    xy1 = dx1/abs(dy1)
    xy2 = dx2/abs(dy2)

    print("XY1:", xy1, "XY2", xy2)

    X = xy1 + xy2 >= 0

    print("X",X, "Y", Y)

    return X


def main():
    

    r1 = Line((2,0), angle=np.pi/4)
    

    # for i in range(-2,3,1):

    #     l1 = Line((i,2), (i+4,-2))
    #     print("\n:LINE", l1)

    #     checkIntersection(r1, l1)

    #     plt.plot(*l1.plot())
    #     plt.plot(*r1.plot())

    #     plt.show()


    # for i in range(-2,3,1):

    #     l1 = Line((i,0.5), (i+4,-2))
    #     print("\n:LINE", l1)

    #     checkIntersection(r1, l1)

    #     plt.plot(*l1.plot())
    #     plt.plot(*r1.plot())

    #     plt.show()


    l1 = Line((1,1), (1,-1))
    for i in range(0,12):

        angle = np.pi * i / 6
        
        r1 = Line((0,0), angle = angle)
        checkIntersection(r1, l1)

        plt.plot(*l1.plot())
        plt.plot(*r1.plot())

        plt.show()





if __name__ == "__main__":
    main()