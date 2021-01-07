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
        // std::cout << "\tTEMP: " << tempValue << "\t" << lineList[i].getP1() << endl;
        if(tempValue > maxValue){
            maxValue = tempValue;
            maxPoint = lineList[i].getP1();
        }

    }

    // std::cout << "\tANGLE: " << angle.degrees() << "\tCOS: " << angle.cosine() << "\tSIN: " << angle.sine() << std::endl;
    return maxPoint;

}


// get the intersection points of a ray and the contour by checking each line
vector<Point> Contour::intersection(Point& p, Angle& a){
        
    vector<Point> intersections;

    std::cout << "\tintersections: " << p << "\t" << a << std::endl;
    // check each line for an intersection with the ray
    for(int i = 0; i < lineList.size(); i++){
        std::cout << "\t CHECK >> " << p << "\t" << lineList[i] << "\t" << lineList[i].checkPossibleIntersection(p,a) << endl;
        
        // if the intersection exists, add the point to the list
        // if(lineList[i].checkPossibleIntersection(p,a)){
            // std::cout << "\t\t OUTPUT >> " << p << "\t" << lineList[i] << "\t" << lineList[i].checkPossibleIntersection(p,a) << endl;
 
            Point* temp = lineList[i].intersection(p, a);

            if(temp){
                std::cout << "\t\t OUTPUT >> " << *temp << "\t" << lineList[i] << "\t" << lineList[i].checkPossibleIntersection(p,a) << endl;

                intersections.push_back(*temp);
            }
        // }
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