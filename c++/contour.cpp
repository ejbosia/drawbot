#include "contour.h"
        
Contour::Contour(vector<Line>& lineRef):lineList(lineRef){

}

vector<Point> Contour::intersection(Ray r){
    return {};
}

vector<Point> Contour::intersection(Line l){
    return {};
}

ostream& operator<<(ostream &strm, const Contour &c){
    
    strm << "\nCONTOUR" << endl;

    for(int i = 0; i < c.lineList.size(); i++){
        strm << "\t" << c.lineList[i] << endl;
    }

    return strm;
}