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

double Point::xRotation(Angle& angle){

    Angle a(-angle.getAngle());

    double c = a.cosine();
    double s = a.sine();
    return x * c - y * s;
}

double Point::yRotation(Angle& angle){

    Angle a(-angle.getAngle());

    double c = a.cosine();
    double s = a.sine();

    return x * s + y * c;
}


/*
Translate the point a dx and dy amount
*/
void Point::translate(double dx, double dy){
    x += dx;
    y += dy;
}

/*
Translate the point a distance in the direction of the input angle
*/
void Point::translate(double distance, Angle& angle){
    double s = angle.sine();
    double c = angle.cosine();

    translate(distance * c, distance * s);
}



std::ostream& operator<<(std::ostream &strm, const Point &p){
    return strm << "(" << p.x << "," << p.y << ")";
}