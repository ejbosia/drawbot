
#ifndef LINE_H
#define LINE_H

#include <iostream>
#include <string>

#include "point.h"
#include "angle.h"

class Line{
    
    private:
        Point p1, p2;
        Angle angle;
        double calculateAngle();

    public:
        Line(Point& p1_, Point& p2_);
        // intersection(Ray& ray);
        // intersection(Line& line);

        friend std::ostream& operator<<(std::ostream &strm, const Line &l);

};

#endif