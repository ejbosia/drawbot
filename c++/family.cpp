#include "family.h"

Family::Family(Contour& parent, std::vector<Contour>& children): parentContour(parent), childContours(children){}


// Point getClosestPoint(){

// }

// Point getNextPoint(){

// }



std::vector<Point> Family::generatePath(){
    std::cout << "PATH GENERATION START" << endl;

    std::vector<Point> path;


    return path;

}

std::ostream& operator<<(std::ostream &strm, const Family &f){
    return strm << "FAMILY NOT DONE";
}
