
#ifndef COLORSTRATEGY_H
#define COLORSTRATEGY_H

#include <iostream>
#include <string>
#include <math.h>
#include <algorithm>
#include <vector>
#include <utility>  // pair
#include <opencv2/opencv.hpp>

#include "point.h"
#include "angle.h"


/*
Class of strategies that take in a family of contours and output a vector of paths to fill the contour
*/
class ColorStrategy{

    public:

        virtual ~ColorStrategy() {};
        virtual std::vector<std::vector<Point>> generateTotalPath(Mat& image) = 0;

};


#endif