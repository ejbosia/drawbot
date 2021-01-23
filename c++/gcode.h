

#ifndef GCODE_H
#define GCODE_H

#include <iostream>
#include <string>
#include <math.h>
#include <vector>

#include "point.h"

/*
Class of strategies that take in a family of contours and output a vector of paths to fill the contour
*/
class GCode{
    
    private:
        double scale;
        std::string Z_UP, Z_DOWN;

        std::string commandDraw(double x, double y);
        std::string commandTravel(double x, double y);
        std::string commandDraw(Point p);
        std::string commandTravel(Point p);
        std::string commandUp();
        std::string commandDown();

    public:
        GCode(double scale);

        std::string generateSubPath(std::vector<Point> sub_path);
        std::string generateGCode(std::vector<std::vector<Point>> total_path);
};

#endif