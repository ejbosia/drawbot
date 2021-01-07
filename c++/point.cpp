#include "point.h"

Point::Point(double x, double y){
    this->x = x;
    this->y = y;
}

/*
Return the distance to another point
*/
double Point::distance(Point &other){
    double dx = x - other.x;
    double dy = y - other.y;
    
    return sqrt(pow(dx,2.0) + pow(dy,2.0));
}

std::ostream& operator<<(std::ostream &strm, const Point &p){
    return strm << "(" << p.x << "," << p.y << ")";
}