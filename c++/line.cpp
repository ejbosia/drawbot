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

bool Line::checkOnLine(Point& p){

    double dx = p.x - p1.x;
    double dy = p.y - p1.y;

    double temp = atan2(dy,dx);

    std::cout << "\tCHECK ON LINE: ANGLE: " << angle << "\tTEST ANGLE: " << temp << std::endl;

    // check if the angle of p1 and p is equal
    if(angle == atan2(dy,dx)){
        
        /*
        // OLD METHOD WITH BUGS
        // check if the point is between the two line points
        double lx = p2.x - p1.x; 
        double ly = p2.y - p1.y; 

        std::cout << "\t\tdx:" << dx << "\t\tdy:" << dy << std::endl;
        std::cout << "\t\tlx:" << lx << "\t\tly:" << ly << std::endl;
        std::cout << "\t\tlimit:" << -std::numeric_limits<double>::epsilon() << std::endl;

        bool bx = (fabs(lx)-fabs(dx)) > -2*std::numeric_limits<double>::epsilon();
        bool by = (fabs(ly)-fabs(dy)) > -2*std::numeric_limits<double>::epsilon();
        
        return (bx && by);
        */

        // CHECK DISTANCES

        double distance = p.distance(p1);
        double lineLength = p2.distance(p1);

        std::cout << "\tDISTANCE: " << distance << "\tLINE LENGTH: " << lineLength << std::endl;

        return (distance <= lineLength);
        
    }

    return false;
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

    if(checkOnLine(temp)){
        return new Point(px,py);
    }
    else{
        return NULL;
    }
}


Point* Line::intersection(Line& line){
    if(angle == line.angle){
        return NULL;
    }
    
    double s1 = angle.tangent();

    Point l1 = line.getP1();

    double s2 = line.getAngle().tangent();
    double V = (p1.y - l1.y + s1 * (l1.x - p1.x)) / (s2 - s1);

    double px = l1.x + V;
    double py = l1.y + s2 * V;

    Point temp(px,py);

    if(checkOnLine(temp) && line.checkOnLine(temp)){
        return new Point(px,py);
    }
    else{
        return NULL;
    }
}

std::ostream& operator<<(std::ostream &strm, const Line &l){
    return strm << "LINE: " <<  l.p1 << " " << l.p2 << " " << l.angle;   
}
