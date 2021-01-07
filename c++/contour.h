/*
Contour class

A contour is a vector of lines.

author: ejbosia
*/
#ifndef CONTOUR_H
#define CONTOUR_H

#include <iostream>
#include <string>
#include <vector>

#include "line.h"


using namespace std;


class Contour{

    private:
        vector<Line> lineList;

    public:
        Contour(vector<Line>& lineRef);

        vector<Point> intersection(Point& p, Angle& a);
        vector<Point> intersection(Line& l);

        friend std::ostream& operator<<(std::ostream &strm, const Contour &c);

};


#endif