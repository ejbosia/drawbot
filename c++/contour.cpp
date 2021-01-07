#include "contour.h"
        
Contour::Contour(vector<Line>& lineRef):lineList(lineRef){

}

vector<Point> Contour::intersection(Ray r){
    return {};
}

vector<Point> Contour::intersection(Line l){
    
    vector<Point> intersections;


    // check each line for an intersection
    for(int i = 0; i < lineList.size(); i++){
        
        Point* temp = l.intersection(lineList[i]);
        
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