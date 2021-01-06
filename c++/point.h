
#ifndef POINT_H
#define POINT_H

#include <iostream>
#include <string>
#include <math.h>

class Point{

    private:
        double x;
        double y;

    public:

        Point(double x, double y);

        double getX();
        double getY();

        double distance(Point& other);

        friend std::ostream& operator<<(std::ostream &strm, const Point &p);
};

#endif