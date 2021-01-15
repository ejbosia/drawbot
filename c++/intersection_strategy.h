
#ifndef INTERSECTIONSTRATEGY_H
#define INTERSECTIONSTRATEGY_H

#include <iostream>
#include <string>
#include <math.h>
#include <algorithm>
#include <vector>

#include "point.h"
#include "angle.h"
#include "contour.h"


/*
Class of strategies that take in a contour family and output the important locations.
*/
class IntersectionStrategy{
    public:
        virtual ~IntersectionStrategy() {};
        virtual std::vector<Point> generateIntersectionPoints(Contour contour) = 0;

};

/*
Find the intersection points using horizontal lines only
*/
class HorizontalIntersectionStrategy : public IntersectionStrategy{
    
    private:
        double lineThickness;
    
    public: 
        HorizontalIntersectionStrategy(double lineThickness);

        std::vector<Point> generateIntersectionPoints(Contour contour);
};


#endif
