
#ifndef CONTOURFILLSTRATEGY_H
#define CONTOURFILLSTRATEGY_H

#include <iostream>
#include <string>
#include <math.h>
#include <algorithm>
#include <vector>

#include "point.h"
#include "angle.h"
#include "contour.h"
#include "family.h"
#include "fill_strategy.h"

/*
Fill in the contour family with a grid pattern
*/
class ContourFillStrategy : public FillStrategy{
        
    private:
        double lineThickness;
        Angle angle;
    
    public: 
        ContourFillStrategy(double lineThickness);

        std::vector<Contour> distanceTransform(Contour contour, double distance);

        std::vector<std::vector<Point>> generateTotalPath(Family family);
};


#endif