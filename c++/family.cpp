#include "family.h"

Family::Family(Contour& parent, std::vector<Contour>& children): parentContour(parent), childContours(children){}


Point getClosestPoint(std::vector<Point> intersectionPoints){

}

Point getNextPoint(std::vector<Point> intersectionPoints){

}


// generate the intersection points, starting from the local minima perpendicular to the angle and moving one lineThickness
void Family::generateIntersectionPoints(vector<Point>& intersectionPoints, double lineThickness, Angle& angle){

    // create a deep copy of the angle and rotate perpendicular
    Angle a(angle.getAngle());
    a.rotateAngle(-M_PI/2);

    DEBUG_MSG("TEST ANGLE: " << angle.degrees());

    // get the maximum point in the perpendicular angle
    Point startingPoint = parentContour.getMaximumPoint(a);

    // get the maximum point in the opposite
    a.rotateAngle(M_PI);
    Point endingPoint = parentContour.getMaximumPoint(a);
    double endingXProj = endingPoint.xRotation(a);

    DEBUG_MSG("TRAVEL ANGLE: " << a.degrees());
    DEBUG_MSG("LINE THICKNESS " << lineThickness);

    DEBUG_MSG("STARTING POINT: " << startingPoint);

    std::vector<Point> intersections;    

    int counter = 0;

    while(startingPoint.xRotation(a) < endingXProj){

        // move the starting point one lineThickness perpendicular to the angle
        startingPoint.translate(lineThickness, a);
        counter++;

        // get the intersections (infinite line at the point and angle)
        intersections = parentContour.fastIntersection(startingPoint, angle);
        
        if(intersections.size() % 2 == 1){
            DEBUG_MSG("ITERATION: " << counter << " POINT " << startingPoint << "NUMBER OF INTERSECTIONS: " << intersections.size());
        }
        
        // copy the points to the intersectionPoints vector
        for( Point p : intersections)
            intersectionPoints.push_back(p);

        intersections.clear();
    }

    DEBUG_MSG("ENDING POINT: " << endingPoint);
    DEBUG_MSG("ENDING SIZE: " << intersectionPoints.size());

}


/*
Find the available intersection point - return NULL if no points are available
*/
Point* Family::getAvailablePoint(vector<Point>& intersectionPoints){

    for( Point point : intersectionPoints){
        if(point.available)
            return &point;
    }
    return NULL;
}

/*
Return one path of the family
*/
std::vector<Point> Family::generatePath(std::vector<Point>& intersectionPoints, double lineThickness, Angle& angle){

    std::vector<Point> path;

    // loop until there are no valid next points
    do{


    }while();

    return path;



}

std::vector<std::vector<Point>> Family::generateTotalPath(double lineThickness, Angle& angle){
    std::cout << "PATH GENERATION START" << std::endl;
    std::cout << "\tLINE THICKNESS " << lineThickness << std::endl;
    std::cout << "\tLINE ANGLE     " << angle << std::endl;


    std::vector<std::vector<Point>> total_path;
    std::vector<Point> intersectionPoints;
    
    // create the intersection points
    generateIntersectionPoints(intersectionPoints, lineThickness, angle);


    // get the starting point
    Point* startingPointer = getAvailablePoint(intersectionPoints);
    
    // loop until there are no starting points available
    while(startingPointer){

        total_path.push_back()


        // get a new starting point (that has not been visited)
        startingPointer = getAvailablePoint(intersectionPoints);
    
    }
    // return total_path

    return total_path;

}

std::ostream& operator<<(std::ostream &strm, const Family &f){
    return strm << "FAMILY NOT DONE";
}
