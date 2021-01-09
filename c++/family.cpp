#include "family.h"

Family::Family(Contour& parent, std::vector<Contour>& children): parentContour(parent), childContours(children){}


// Point getClosestPoint(){

// }

// Point getNextPoint(){

// }


// generate the intersection points, starting from the local minima perpendicular to the angle and moving one lineThickness
void Family::generateIntersectionPoints(double lineThickness, Angle& angle){

    // create a deep copy of the angle and rotate perpendicular
    Angle a(angle.getAngle());
    a.rotateAngle(-M_PI/2);

    DEBUG_MSG("TEST ANGLE: " << angle.degrees() << " new: " << a.degrees());

    // get the maximum point in the perpendicular angle
    Point startingPoint = parentContour.getMaximumPoint(a);

    // get the maximum point in the opposite
    a.rotateAngle(M_PI);
    Point endingPoint = parentContour.getMaximumPoint(a);
    double endingXProj = endingPoint.xRotation(a);

    DEBUG_MSG("TRAVEL ANGLE: " << a.degrees());

    DEBUG_MSG("STARTING POINT: " << startingPoint);


    std::vector<Point> intersections;    

    while(startingPoint.xRotation(a) < endingXProj){

        // move the starting point one lineThickness perpendicular to the angle
        startingPoint.translate(lineThickness, a);

        DEBUG_MSG("TRANSLATION: " << startingPoint << "\t" << angle);

        // check one direction
        // angle.rotateAngle(M_PI);

        // std::cout << "\tANGLE " << angle << std::endl;

        intersections = parentContour.intersection(startingPoint, angle);

        // // check the other direction
        // angle.rotateAngle(M_PI);

        // std::cout << "\tANGLE " << angle << std::endl;

        // negIntersections = parentContour.intersection(startingPoint, angle);

        DEBUG_MSG("INTERSECTIONS SIZE: " << intersections.size());
        // std::cout << negIntersections.size() << std::endl;
        
        for(int i = 0; i < intersections.size(); i++)
            DEBUG_MSG("\tPOINT" << intersections[i]);

        // std::cout << "\t";

        // for(int i = 0; i < negIntersections.size(); i++)
        //     std::cout << negIntersections[i] << ", ";
        
        // posIntersections.clear();
        // negIntersections.clear();

    }

    DEBUG_MSG("ENDING POINT: " << endingPoint);




}


std::vector<std::vector<Point>> Family::generatePath(double lineThickness, Angle& angle){
    std::cout << "PATH GENERATION START" << std::endl;
    std::cout << "\tLINE THICKNESS " << lineThickness << std::endl;
    std::cout << "\tLINE ANGLE     " << angle << std::endl;


    std::vector<std::vector<Point>> path;


    // create the intersection points
    generateIntersectionPoints(lineThickness, angle);

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
