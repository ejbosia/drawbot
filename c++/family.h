
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

        void generateIntersectionPoints(double lineThickness, Angle& angle);

    public:
        Family(Contour& parent, std::vector<Contour>& children);


        // Point getClosestPoint();

        // Point getNextPoint();

        // vector<Point> intersection(Ray& ray);
        std::vector<std::vector<Point>> generatePath(double lineThickness, Angle& angle);

        friend std::ostream& operator<<(std::ostream &strm, const Family &f);
};

#endif