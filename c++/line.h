
#ifndef LINE_H
#define LINE_H

#include <iostream>
#include <string>
#include <math.h>
#include <cmath>
#include <limits>

#include "point.h"
#include "angle.h"

#if defined(DEBUG) || defined(DEBUG_LINE)
#define DEBUG_MSG_L(str) do { std::cout << "DEBUG LINE\t" << str << std::endl; } while( false )
#else
#define DEBUG_MSG_L(str) do { } while ( false )
#endif

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

        Point* midPoint();

        // vector<Point> intersection(Ray& ray);

        bool checkOnLine(Point& p);

        bool checkEndPointIntersection(Point& p, Angle& a);
        bool checkPossibleIntersection(Point& p, Angle& a);
        bool checkPossibleIntersection(Line& line);

        Point* intersection(Point& p, Angle& a);
        Point* intersection(Line& line);

        friend std::ostream& operator<<(std::ostream &strm, const Line &l);
};

#endif