#include "family.h"

Family::Family(Contour& parent, std::vector<Contour>& children): parentContour(parent), childContours(children){}


// Point getClosestPoint(){

// }

// Point getNextPoint(){

// }



std::vector<std::vector<Point>> Family::generatePath(){
    std::cout << "PATH GENERATION START" << endl;

    std::vector<std::vector<Point>> path;


    // create the intersection points
    // self.generate_intersection_points(line_thickness, angle)

    // loop until some stop iteration (no paths remaining)
    //while not path is None:

    //     path = self.generate_path(line_thickness, angle)
    
    // add the path to the list
    //     if not path is None:
    //         total_path.append(path)

    // return total_path

    return path;

}

std::ostream& operator<<(std::ostream &strm, const Family &f){
    return strm << "FAMILY NOT DONE";
}
