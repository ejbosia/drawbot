#include "line.h"

Line::Line(Point& p1_, Point& p2_): p1(p1_), p2(p2_), angle(calculateAngle()){}


double Line::calculateAngle(){
    
    double dx = p2.getX() - p1.getX();
    double dy = p2.getY() - p1.getY();
    
    return atan2(dy,dx);
}

Point Line::getP1(){
    return p1;
}

Point Line::getP2(){
    return p2;
}

Angle Line::getAngle(){
    return angle;
}

Point* Line::intersection(Line& line){
    if(angle == line.angle){
        return NULL;
    }
    
    double s1 = angle.tangent();

    Point l1 = line.getP1();

    double s2 = line.getAngle().tangent();
    double V = (p1.getY() - l1.getY() + s1 * (l1.getX() - p1.getX())) / (s2 - s1);

    double px = l1.getX() + V;
    double py = l1.getY() + s2 * V;

    return new Point(px, py);
}

std::ostream& operator<<(std::ostream &strm, const Line &l){
    return strm << "LINE: " <<  l.p1 << " " << l.p2 << " " << l.angle;   
}
