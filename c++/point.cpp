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

std::string Point::toString(){
    return "(" + std::to_string(x) + "," + std::to_string(y) + ")";
}