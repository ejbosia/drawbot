#include "point.h"
#include "angle.h"
#include "ray.h"

Ray::Ray(Point& p, Angle& a): p1(p), angle(a){
    
}

Point Ray::getPoint(){
    return p1;
}

Angle Ray::getAngle(){
    return angle;
}

std::ostream& operator<<(std::ostream &strm, const Ray &r){
    return strm << "RAY: " <<  r.p1 << " " << r.angle;   
}

