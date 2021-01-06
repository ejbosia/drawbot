#include "point.h"

Point::Point(double x, double y){
    this->x = x;
    this->y = y;
}

double Point::getX(){
    return x;
}

double Point::getY(){
    return y;
}

/*
Return the distance to another point
*/
double Point::distance(Point &other){
    double dx = x - other.getX();
    double dy = y - other.getY();
    
    return sqrt(pow(dx,2.0) + pow(dy,2.0));
}

std::ostream& operator<<(std::ostream &strm, const Point &p){
    return strm << "(" << p.x << "," << p.y << ")";
}