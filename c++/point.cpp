#include "point.h"

Point::Point(double x, double y){
    this->x = x;
    this->y = y;
}

/*
Return the distance to another point
*/
double distance(const Point &other){
    double dx = x - other.getX();
    double dx = y - other.getY();
    
    return 0.0 // TODO CALCULATE DISTANCE

}

std::ostream& operator<<(std::ostream &strm, const Point &p){
    return strm << "(" << p.x << "," << p.y << ")";
}