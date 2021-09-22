import utilities.shapely_utilities as SU

from shapely.geometry import LineString, Point

EPSILON = 1e-8


def generate_linestrings():
    '''
    Create a list of linestrings for testing
    '''
    pass


def test_distance_transform():
    '''
    Test the distance transform
    '''
    pass


def test_cut():
    '''
    Cut a linestring at a specified distance. This always returns at least one linestring and a None, or two linestrings
    '''
    # create a linestring
    ls = LineString([(0, 0), (10, 0), (10, 10), (20, 10)])

    # test a normal cut
    start, end = SU.cut(ls, 15)

    assert start.length == 15
    assert end.length == ls.length - 15
    assert start.coords[-1] == end.coords[0]

    # test cutting on the start
    start, end = SU.cut(ls, 0)
    assert start is None
    assert end == ls

    # test cutting on the end
    start, end = SU.cut(ls, ls.length)
    assert start == ls
    assert end is None

    # test cutting a negative distance
    start, end = SU.cut(ls, -1)
    assert start is None
    assert end == ls

    # test cutting farther than the length
    start, end = SU.cut(ls, ls.length+1)
    assert start == ls
    assert end is None


# return the length of the linestring, including the straightline distance from start to end
def get_cycle_length(ls):
    return ls.length + Point(ls.coords[0]).distance(Point(ls.coords[-1]))


def test_cycle():
    '''
    Reformat the linestring so position 0 is the start point. This may involve inserting a new point into the contour.
    '''

    # create a linestring
    ls = LineString([(0, 0), (10, 0), (10, 10), (0, 10)])

    # test normal cycle
    output = SU.cycle(ls, 15)
    assert get_cycle_length(output) == get_cycle_length(ls)
    assert Point(output.coords[0]) == ls.interpolate(15)

    # test cycle past end of linestring (similar to x rotations + some distance)
    output = SU.cycle(ls, ls.length+15)
    assert get_cycle_length(output) == get_cycle_length(ls)
    assert Point(output.coords[0]) == ls.interpolate(15)

    # test negative cycle ()
    output = SU.cycle(ls, -15)
    assert get_cycle_length(output) == get_cycle_length(ls)
    assert Point(output.coords[0]) == ls.interpolate(ls.length-15)

    # test cycle on start (does nothing)
    assert ls == SU.cycle(ls, 0)

    # test cycle on end (does nothing)
    assert ls == SU.cycle(ls, ls.length)


def test_self_intersections():
    '''
    Find any self intersections in the input linestring
    '''
    no_intersection = LineString([(0, 0), (5, 5), (0, 1)])

    assert no_intersection.is_simple
    assert not SU.self_intersections_binary(no_intersection)


def test_self_intersections_binary():
    '''
    Find any self intersections in the input linestring
    '''
    no_intersection = LineString([(0, 0), (5, 5), (0, 1)])

    assert no_intersection.is_simple
    assert not SU.self_intersections_binary(no_intersection)


def test_reverse():
    '''
    Reverse a input linestring ~ this is helpful for projection when the distance is ambiguous (intersections)
    '''
    ls = LineString([(0, 0), (10, 0), (10, 10), (20, 10)])

    assert ls.coords[::-1] == list(SU.reverse(ls).coords)


def test_merge():
    '''
    Merge two linestrings
    '''

    ls = LineString([(0, 0), (10, 0), (10, 10), (20, 10)])

    start, end = SU.cut(ls, 15)

    output = SU.merge(start, end)

    assert output.length == ls.length
    assert output.coords[0] == ls.coords[0]
    assert output.coords[-1] == ls.coords[-1]


def test_sample():

    SAMPLE_DIS = 1.0

    ls = LineString([(0, 0), (10, 0), (10, 10), (20, 10)])

    points = SU.sample(ls, SAMPLE_DIS)

    # check the start point is included in the sample
    assert points.coords[0] == ls.coords[0]

    # check that the last point is within the sample distance from the end
    assert ls.length - points.length <= SAMPLE_DIS + 1e-8

    # check that the projection distances between points are correct
    p0 = None
    for p1 in points.coords:
        p1 = Point(p1)
        if p0 is not None:

            # check that the points are the correct sample distance apart
            assert abs(ls.project(p1) - ls.project(p0) - SAMPLE_DIS) < EPSILON

        p0 = Point(p1)

        # check that the point is on the line
        assert ls.distance(p0) < EPSILON


def test_virtual_boundary():
    pass
