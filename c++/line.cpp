#include "line.h"
#include <math.h>

Line::Line(Point& p1_, Point& p2_): p1(p1_), p2(p2_),angle(calculateAngle()){

}


double Line::calculateAngle(){
    
    double dx = p2.getX() - p1.getX();
    double dy = p2.getY() - p1.getY();
    
    return atan2(dy,dx);
}


std::ostream& operator<<(std::ostream &strm, const Line &l){
    return strm << "LINE: " <<  l.p1 << " " << l.p2 << " " << l.angle;   
}
