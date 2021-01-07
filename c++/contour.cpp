#include "contour.h"
        
Contour::Contour(vector<Line>& lineRef):lineList(lineRef){

}


// get the intersection points of a ray and the contour by checking each line
vector<Point> Contour::intersection(Point& p, Angle& a){
        
    vector<Point> intersections;

    // check each line for an intersection with the ray
    for(int i = 0; i < lineList.size(); i++){
        
        Point* temp = lineList[i].intersection(p, a);
        
        if(temp){
            intersections.push_back(*temp);
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