#include "family.h"

Family::Family(Contour& parent, std::vector<Contour>& children): parentContour(parent), childContours(children){}

/*
Point getClosestPoint(std::vector<Point> intersectionPoints){

}

Point getNextPoint(std::vector<Point> intersectionPoints){

}
*/


/*
Rotate all of the contours about (0,0)
*/
void Family::rotate(Angle& angle){

    parentContour.rotate(angle);

    for(int i = 0; i < childContours.size(); i++){
        childContours[i].rotate(angle);
    }

}


// generate the intersection points, starting from the local minima perpendicular to the angle and moving one lineThickness
void Family::generateIntersectionPoints(vector<Point>& intersectionPoints, double lineThickness, Angle& angle){

    // create a deep copy of the angle and rotate perpendicular
    Angle reverse(-angle.getAngle());

    // rotate the to make the line perpendicular
    rotate(reverse);

    intersectionPoints = parentContour.getIntersectionPointsTraverse(lineThickness);

    std::cout << "x=[";
    for(int i = 0; i < intersectionPoints.size(); i++){
        cout << intersectionPoints[i].x << ", ";
    }
    std::cout << "]" << std::endl << "y=[";
    for(int i = 0; i < intersectionPoints.size(); i++){
        cout << intersectionPoints[i].y << ", ";
    }
    std::cout << "]" << std::endl;

    for(int i = 0; i < intersectionPoints.size(); i++){
        intersectionPoints[i].rotate(angle);
        DEBUG_MSG("RESULT: " << intersectionPoints[i]);
    }

    std::cout << "x=[";
    for(int i = 0; i < intersectionPoints.size(); i++){
        cout << intersectionPoints[i].x << ", ";
    }
    std::cout << "]" << std::endl << "y=[";
    for(int i = 0; i < intersectionPoints.size(); i++){
        cout << intersectionPoints[i].y << ", ";
    }
    std::cout << "]" << std::endl;


    rotate(angle);
    DEBUG_MSG("ENDING SIZE: " << intersectionPoints.size());

}


/*
Find the available intersection point - return NULL if no points are available
*/
Point* Family::getAvailablePoint(vector<Point>& intersectionPoints){

    for(int i = 0; i < intersectionPoints.size(); i++){
        if(intersectionPoints[i].available)
            return &(intersectionPoints[i]);
    }
    return NULL;
}

/*
Return one path of the family
*/
std::vector<Point> Family::generatePath(std::vector<Point>& intersectionPoints, double lineThickness, Angle& angle){

    std::vector<Point> path;
    bool next_point = false;

    // loop until there are no valid next points
    do{


    }while(next_point);

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
    
    /*
    while(startingPointer){

        DEBUG_MSG(*startingPointer);
        // get a new starting point (that has not been visited)
        startingPointer = getAvailablePoint(intersectionPoints);

    
    }
    */
    // return total_path

    return total_path;

}

std::ostream& operator<<(std::ostream &strm, const Family &f){
    return strm << "FAMILY NOT DONE";
}
