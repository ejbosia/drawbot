
#ifndef GRIDFILLSTRATEGY_H
#define GRIDFILLSTRATEGY_H

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
#include "fill_strategy.h"
#include "intersection_strategy.h"

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


#endif