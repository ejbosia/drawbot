
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
#include <algorithm>
#include <vector>

#include "point.h"
#include "contour.h"

class Family{
    
    private:
        std::vector<Contour> contours;  // parent contour is the first contour

        std::map<int, std::vector<Point>> rowIntersectionMap;

        void generateIntersectionPoints(double lineThickness, Angle& angle);

        Point* getAvailablePoint();

        std::vector<Point> generatePath(Point startPoint);

    public:
        Family(std::vector<Contour>& children);

        void rotate(Angle& angle);

        bool getAcrossPoint(Point& point);
        bool getNextPoint(Point& point);

        std::vector<std::vector<Point>> generateTotalPath(double lineThickness, Angle& angle);

        friend std::ostream& operator<<(std::ostream &strm, const Family &f);
};

#endif