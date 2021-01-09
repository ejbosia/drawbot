/*
Contour class

A contour is a vector of lines.

author: ejbosia
*/
#ifndef CONTOUR_H
#define CONTOUR_H

#ifdef DEBUG
#define DEBUG_MSG(str) do { std::cout << "DEBUG CONTOUR\t" << str << std::endl; } while( false )
#else
#define DEBUG_MSG(str) do { } while ( false )
#endif

#include <iostream>
#include <string>
#include <vector>
#include <map>

#include "line.h"

using namespace std;


class Contour{

    private:
        vector<Line> lineList;
        vector<Point> intersectionPoints;
        map<int,vector<int>> rowIntersectionPointMap;

    public:
        Contour(vector<Line>& lineRef);

        Point getMaximumPoint(Angle& angle);

        vector<Point> intersection(Point& p, Angle& a);
        vector<Point> intersection(Line& l);

        friend std::ostream& operator<<(std::ostream &strm, const Contour &c);

};


#endif