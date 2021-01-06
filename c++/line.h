
#ifndef LINE_H
#define LINE_H

#include <iostream>
#include <string>
#include <math.h>

#include "point.h"
#include "angle.h"
#include "ray.h"

class Line{
    
    private:
        Point p1, p2;
        Angle angle;
        double calculateAngle();

    public:
        Line(Point& p1_, Point& p2_);

        Point getP1();
        Point getP2();
        Angle getAngle();

        // vector<Point> intersection(Ray& ray);
        Point* intersection(Line& line);

        friend std::ostream& operator<<(std::ostream &strm, const Line &l);
};

#endif