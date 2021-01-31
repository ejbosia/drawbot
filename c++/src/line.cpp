#include "line.h"

Line::Line(Point& p1_, Point& p2_): p1(p1_), p2(p2_), angle(calculateAngle()){}


double Line::calculateAngle(){
    
    double dx = p2.x - p1.x;
    double dy = p2.y - p1.y;
    
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


Point* Line::midPoint(){
    double px = (p2.x+p1.x)/2;
    double py = (p2.y+p1.y)/2;

    return new Point(px,py);
}

bool Line::checkOnLine(Point& p){

    double dx = p.x - p1.x;
    double dy = p.y - p1.y;

    double temp = atan2(dy,dx);

    //DEBUG_MSG_L("ANGLE: " << temp << "\t" << angle);

    // check if the angle of p1 and p is equal
    if(angle == atan2(dy,dx)){

        // CHECK DISTANCES

        double distance = p.distance(p1);
        double lineLength = p2.distance(p1);

        return (distance <= lineLength);
        
    }

    return false;
}


/*
Check if line lies on each side of the input ray
*/
bool Line::checkEndPointIntersection(Point& p, Angle& a){
    
    // create two temporary points for the line endpoints
    Point temp1(p1.x,p1.y);
    Point temp2(p2.x,p2.y);

    temp1.translate(-p.x,-p.y);
    temp2.translate(-p.x,-p.y);

    DEBUG_MSG_L(temp1 << "\t" << temp2);

    // rotate the temp points to match the ray
    Angle reverse(-a.getAngle());
    temp1.rotate(reverse);
    temp2.rotate(reverse);
    
    DEBUG_MSG_L(temp1 << "\t" << temp2  << "\t" << reverse.degrees());
    
    // if the sign of each y component are the same, intersection is impossible
    return temp1.y * temp2.y <= 0.0f;
}


/*
Check if an input ray (point and angle) could intersect the line
*/
bool Line::checkPossibleIntersection(Point& p, Angle& a){

    // create two temporary points for the line endpoints
    Point temp1(p1.x,p1.y);
    Point temp2(p2.x,p2.y);

    temp1.translate(-p.x,-p.y);
    temp2.translate(-p.x,-p.y);
    DEBUG_MSG_L("TEMP1: " <<  temp1 << " TEMP2:" << temp2);

    // rotate the temp points to match the ray
    Angle reverse(-a.getAngle());
    temp1.rotate(reverse);
    temp2.rotate(reverse);

    DEBUG_MSG_L("TEMP1: " <<  temp1 << " TEMP2:" << temp2);
    // if the sign of each y component are the same, intersection is impossible
    if(temp1.y * temp2.y > 0.0f){
        return false;
    }

    /*
    X check
     - check the x normalized to y sum is greater than 0
     - the ray is currently at angle 0, so lines that have negative weight have an intersection point in -x
    */

    double normal1 = temp1.x/fabs(temp1.y);
    double normal2 = temp2.x/fabs(temp2.y);

    DEBUG_MSG_L("NORMAL1: " <<  normal1 << " NORMAL2:" << normal2);

    return (normal1 + normal2 > 0);

}


bool Line::checkPossibleIntersection(Line& line){

    Point temp = line.getP1();
    Angle angle = line.getAngle();

    // check if the ray condition holds for each line
    return checkPossibleIntersection(temp,angle) && line.checkPossibleIntersection(p1, angle);
}


// check if an input ray intersects with the line
Point* Line::intersection(Point& p, Angle& a){
        
    if(angle == a){
        return NULL;
    }
    
    double s1 = angle.tangent();
    double s2 = a.tangent();

    double V = (p1.y - p.y + s1 * (p.x - p1.x)) / (s2 - s1);

    double px = p.x + V;
    double py = p.y + s2 * V;

    Point temp(px,py);

    DEBUG_MSG_L(temp << checkOnLine(temp));

    return new Point(px,py);
    /*
    if(checkOnLine(temp)){
        return new Point(px,py);
    }
    else{
        return NULL;
    }
    */
}

// find the intersection point between this line and another line ~ return NULL if the intersection point is not on the lines
Point* Line::intersection(Line& line){
    
    // get the result if the input line is a ray

    Point p = line.getP1();
    Angle a = line.getAngle();

    Point* result = intersection(p,a);

    if(result){
        
        // if there is a point, and that point is not on the input line, then return NULL (no intersecting points)
        if(!line.checkOnLine(*result))
            result = NULL;
    }

    return result;
}

std::ostream& operator<<(std::ostream &strm, const Line &l){
    return strm << "LINE: " <<  l.p1 << " " << l.p2 << " " << l.angle;   
}
