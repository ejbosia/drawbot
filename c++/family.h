
#ifndef FAMILY_H
#define FAMILY_H

#if defined(DEBUG) || defined(DEBUG_FAMILY)
#define DEBUG_MSG(str) do { std::cout << "DEBUG FAMILY\t" << str << std::endl; } while( false )
#else
#define DEBUG_MSG(str) do { } while ( false )
#endif


#include <iostream>
#include <string>
#include <math.h>

#include "point.h"
#include "contour.h"

class Family{
    
    private:
        Contour parentContour;
        std::vector<Contour> childContours;

        void generateIntersectionPoints(vector<Point>& intersectionPoints, double lineThickness, Angle& angle);
        Point* getAvailablePoint(vector<Point>& intersectionPoints);

        std::vector<Point> generatePath(std::vector<Point>& intersectionPoints, double lineThickness, Angle& angle);

    public:
        void rotate(Angle& angle);


        Family(Contour& parent, std::vector<Contour>& children);

        // Point getClosestPoint();
        // Point getNextPoint();

        std::vector<std::vector<Point>> generateTotalPath(double lineThickness, Angle& angle);

        friend std::ostream& operator<<(std::ostream &strm, const Family &f);
};

#endif