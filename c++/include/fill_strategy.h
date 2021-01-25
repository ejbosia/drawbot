
#ifndef FILLSTRATEGY_H
#define FILLSTRATEGY_H

#include <iostream>
#include <string>
#include <math.h>
#include <algorithm>
#include <vector>
#include <utility>  // pair

#include "point.h"
#include "angle.h"
#include "contour.h"
#include "family.h"
#include "intersection_strategy.h"

/*
Class of strategies that take in a family of contours and output a vector of paths to fill the contour
*/
class FillStrategy{
    protected:
        IntersectionStrategy* intersectionStrategy;

    public:

        virtual ~FillStrategy() {};
        virtual std::vector<std::vector<Point>> generateTotalPath(Family family) = 0;

};

/*
Fill in the contour family with a grid pattern
*/
class GridFillStrategy : public FillStrategy{
        
    private:
        double lineThickness;
        Angle angle;
    
    public: 
        GridFillStrategy(double lineThickness, Angle angle);

        std::vector<std::vector<Point>> generateTotalPath(Family family);
};


/*
Fill in the contour family with a star pattern
*/
class StarFillStrategy : public FillStrategy{
        
    private:
        double lineThickness;
        Angle angle;
    
    
    public: 

        StarFillStrategy(double lineThickness, Angle angle);

        std::vector<std::vector<Point>> generateTotalPath(Family family);
};


#endif