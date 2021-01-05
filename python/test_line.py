import pytest
import os
import math

# setup the logging level for testing
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


from line import Line


def test_length():
    p1 = (0,0)
    p2 = (3,4)
    
    l = Line(p1, p2=p2)

    assert l.length() == 5


def test_angle():
    p1 = (0,0)
    p2 = (1,1)

    l = Line(p1, p2=p2)

    assert l.angle == (math.pi/4)

    


def test_intersection():

    l1 = Line((0,0), p2=(10,10))
    l2 = Line((10,0), p2=(0,10))
    l3 = Line((10,0), (6,4))

    r1 = Line((5,0), angle = math.pi/2)
    r2 = Line((5,0), angle = -math.pi/2)

    # normal intersection (both ways)
    assert l1.intersection(l2) == (5,5)
    assert l2.intersection(l1) == (5,5)

    # same line ~ return None because they are parallel
    assert l1.intersection(l1) is None

    # directions correct, but lines do not intersect
    assert l1.intersection(l3) is None
    assert l3.intersection(l1) is None

    # ray intersection with line
    assert l1.intersection(r1) == (5,5)
    assert r1.intersection(l1) == (5,5)

    # ray not intersecting with line
    assert l1.intersection(r2) is None
    assert r2.intersection(l1) is None


