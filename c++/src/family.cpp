#include "family.h"

Family::Family(std::vector<Contour>& children): contours(children){}


/*
Return the contour at the input index
*/
Contour Family::get(int index){
    return contours[index];
}


/*
Return the number of contours in the family
*/
int Family::size(){
    return contours.size();
}


/*
Rotate all of the contours about (0,0)
*/
void Family::rotate(Angle& angle){

    for(int i = 0; i < contours.size(); i++){
        contours[i].rotate(angle);
    }
}


/*
Format the family for printing
*/
std::ostream& operator<<(std::ostream &strm, const Family &f){
    return strm << "FAMILY NOT DONE";
}
