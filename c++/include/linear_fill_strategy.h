
#ifndef LINEARFILLSTRATEGY_H
#define LINEARFILLSTRATEGY_H

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
Fill in the contour family with back and forth lines
*/
class LinearFillStrategy : public FillStrategy{
        
    private:
        double lineThickness;
        Angle angle;

        std::vector<std::vector<Point>> intersectionPoints;
        std::map<int, std::vector<Point*>> rowIntersectionMap;

        void initRowIntersectionMap();

        void findPoint(Point* newPtr, int& contour, int& index);
        void getAcrossPoint(int& contour, int& index);
        void getNextPoint(int& contour, int& index);
        void getAvailablePoint(int& contour, int& index);


        std::vector<Point> generatePath(int& contour, int& index);
    
    public: 
        LinearFillStrategy(double lineThickness, Angle angle);

        std::vector<std::vector<Point>> generateTotalPath(Family family);
};

#endif