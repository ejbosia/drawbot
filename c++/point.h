
#ifndef POINT_H
#define POINT_H

#include <iostream>
#include <string>
#include <math.h>

#include "angle.h"

class Point{

    public:
        double x;
        double y;
        bool available;
        
        Point(double x, double y);

        double distance(Point& other);
        Angle angle(Point& other);

        double xRotation(Angle& angle);
        double yRotation(Angle& angle);


        // point translation
        void translate(double distance, Angle& angle);
        void translate(double dx, double dy);

        void rotate(Angle& angle);
        void rotate(Point& point, Angle& angle);


        bool operator==(const Point &p);
        Point operator-(const Point &p);

        friend std::ostream& operator<<(std::ostream &strm, const Point &p);
};

#endif