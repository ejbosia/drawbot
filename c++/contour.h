/*
Contour class

A contour is a vector of lines.

author: ejbosia
*/
#ifndef CONTOUR_H
#define CONTOUR_H

#if defined(DEBUG) || defined(DEBUG_CONTOUR)
#define DEBUG_MSG_C(str) do { std::cout << "DEBUG CONTOUR\t" << str << std::endl; } while( false )
#else
#define DEBUG_MSG_C(str) do { } while ( false )
#endif

#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <algorithm>

#include "line.h"

using namespace std;


class Contour{

    private:
        vector<Point> vertexList;

    public:

        // vertexList accessor functions
        Point get(int index);
        int size();



        int getStartingIndex(Point& p);

        int getFirstAvailable();

        Contour(vector<Point>& vertexList);

        Point getMaximumPoint(Angle& angle);

        Point* traverse(Point& p, double distance, bool clockwise=true);

        int findIntersectionPointIndex(Point& p);


        void rotate(Angle& angle);

        friend std::ostream& operator<<(std::ostream &strm, const Contour &c);

};


#endif