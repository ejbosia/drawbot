
#ifndef POINT_H
#define POINT_H

#include <iostream>
#include <string>
#include <math.h>

class Point{

    public:
        double x;
        double y;
        
        Point(double x, double y);

        double getX();
        double getY();

        double distance(Point& other);

        friend std::ostream& operator<<(std::ostream &strm, const Point &p);
};

#endif