import pytest
import os


from line import Line


def test_length():
    p1 = (0,0)
    p2 = (3,4)
    
    l = Line(p1, p2=p2)

    print(l.length())


def test_angle():
    p1 = (0,0)
    p2 = (1,1)

    l = Line(p1, p2=p2)

    print(l.angle)


def test_intersection():

    l1 = Line((0,0), p2=(10,10))
    l2 = Line((10,0), p2=(0,10))

    print(l1.intersection(l2))
