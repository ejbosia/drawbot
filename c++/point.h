
#ifndef POINT_H
#define POINT_H

#include <iostream>
#include <string>

class Point{

    private:
        int x;
        int y;

    public:

        Point(int x, int y);

        int getX();
        int getY();

        friend std::ostream& operator<<(std::ostream &strm, const Point &p);
};

#endif