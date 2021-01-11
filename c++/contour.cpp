#include "contour.h"
        
Contour::Contour(vector<Line>& lineRef):lineList(lineRef){

}

// get the maximum point in the contour in the direction of the angle
Point Contour::getMaximumPoint(Angle& angle){

    Point maxPoint = lineList.front().getP1();
    double maxValue = maxPoint.xRotation(angle);

    double tempValue;

    for(int i = 0; i < lineList.size(); i++){
        
        tempValue = lineList[i].getP1().xRotation(angle);
        DEBUG_MSG_C("TEMP: " << tempValue << "\t" << lineList[i].getP1());;
        if(tempValue > maxValue){
            maxValue = tempValue;
            maxPoint = lineList[i].getP1();
        }

    }

    DEBUG_MSG_C("ANGLE: " << angle.degrees() << "\tCOS: " << angle.cosine() << "\tSIN: " << angle.sine());
    return maxPoint;

}


// get the intersection point for an infinite line
vector<Point> Contour::fastIntersection(Point& p, Angle& a){
        
    vector<Point> intersections;
    
    // check each line for an intersection with the ray
    for(int i = 0; i < lineList.size(); i++){

        // if the intersection exists, add the point to the list
        if(lineList[i].checkEndPointIntersection(p,a)){
            DEBUG_MSG_C("LINE: " << lineList[i]);

            Point* temp = lineList[i].intersection(p, a);

            if(temp){
                intersections.push_back(*temp);
            }
            
            delete temp;
        }
    }

    return intersections;
}



// get the intersection points of a ray and the contour by checking each line
vector<Point> Contour::intersection(Point& p, Angle& a){
        
    vector<Point> intersections;

    DEBUG_MSG_C("intersections: " << p << "\t" << a);
    
    // check each line for an intersection with the ray
    for(int i = 0; i < lineList.size(); i++){
        
        // DEBUG_MSG_C("CHECK >> " << p << "\t" << lineList[i] << "\t" << lineList[i].checkPossibleIntersection(p,a));
        
        // if the intersection exists, add the point to the list
         if(lineList[i].checkPossibleIntersection(p,a)){
            
            // DEBUG_MSG_C("OUTPUT >> " << p << "\t" << lineList[i] << "\t" << lineList[i].checkPossibleIntersection(p,a));
 
            Point* temp = lineList[i].intersection(p, a);

            if(temp){
                // DEBUG_MSG_C("\t\t OUTPUT >> " << *temp << "\t" << lineList[i] << "\t" << lineList[i].checkPossibleIntersection(p,a));

                intersections.push_back(*temp);
            }
            
            delete temp;
        }
    }

    return intersections;
}


vector<Point> Contour::intersection(Line& l){
    
    vector<Point> intersections;

    // check each line for an intersection
    for(int i = 0; i < lineList.size(); i++){
        
        Point* temp = lineList[i].intersection(l);
        
        if(temp){
            intersections.push_back(*temp);
        }
    }

    return intersections;
}

ostream& operator<<(ostream &strm, const Contour &c){
    
    strm << "\nCONTOUR" << endl;

    for(int i = 0; i < c.lineList.size(); i++){
        strm << "\t" << c.lineList[i] << endl;
    }

    return strm;
}