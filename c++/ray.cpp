#include "point.h"
#include "angle.h"
#include "ray.h"

Ray::Ray(Point& p, Angle& a): point(p), angle(a){
    
}

std::ostream& operator<<(std::ostream &strm, const Ray &r){
    return strm << "RAY: " <<  r.point << " " << r.angle;   
}

