#include "point.h"

Point::Point(int x, int y){
    this->x = x;
    this->y = y;
    setVisited(false);
}

int Point::getX(){
    return x;
}

int Point::getY(){
    return y;
}

void Point::setVisited(bool v){
    visited = v;
}

bool Point::getVisited(){
    return visited;
}

std::ostream& operator<<(std::ostream &strm, const Point &p){
    return strm << "(" << p.x << "," << p.y << ")";
}