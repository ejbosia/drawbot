
#ifndef POINT_H
#define POINT_H

#include <iostream>
#include <string>

class Point{

    private:
        int x;
        int y;
        bool visited;

    public:

        Point(int x, int y);

        int getX();
        int getY();

        void setVisited(bool visited);
        bool getVisited();

        std::string toString();
};

#endif