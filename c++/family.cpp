#include "family.h"

Family::Family(std::vector<Contour>& children): contours(children){}

struct less_than_x
{
    inline bool operator() (const Point& p1, const Point& p2)
    {
        return (p1.x < p2.x);
    }
};


/*
Rotate all of the contours about (0,0)
*/
void Family::rotate(Angle& angle){

    for(int i = 0; i < contours.size(); i++){
        contours[i].rotate(angle);
    }

}


// generate the intersection points, starting from the local minima perpendicular to the angle and moving one lineThickness
void Family::generateIntersectionPoints(double lineThickness, Angle& angle){

    // create a deep copy of the angle and rotate perpendicular
    Angle reverse(-angle.getAngle());

    // rotate the to make the line perpendicular
    rotate(reverse);

    int row;

    // get the intersection points for each contour, and add them to the map
    for(int i = 0 ; i < contours.size(); i++){
        for(Point p : contours[i].getIntersectionPointsTraverse(lineThickness)){
            row = (int)(p.y/lineThickness);
            
            // if the row has not been created yet initialize an empty vector
            if(rowIntersectionMap.find(row) == rowIntersectionMap.end()){
                rowIntersectionMap.insert(std::pair<int, std::vector<Point>>(row, std::vector<Point>()));
            }

            rowIntersectionMap.at(row).push_back(p);
        }
        std::cout << contours[i].intersectionPoints.size() << std::endl;
    }
    std::cout << contours[0].intersectionPoints.size() << std::endl;


    DEBUG_MSG("ENDING SIZE: " << intersectionPoints.size());

}


/*
Find the available intersection point - return NULL if no points are available
*/
Point* Family::getAvailablePoint(){

    int index; 
    for(Contour c : contours){

        index = c.getFirstAvailable();

        if(index != -1){
            return c.getIntersectionPoint(index);
        }
    }
    return NULL;
}

/*
Get the point across the contour
*/
bool Family::getAcrossPoint(Point& point){

    int row = (int)point.y;
    int index;

    // find the index of the point
    std::vector<Point>::iterator it = find(rowIntersectionMap[row].begin(), rowIntersectionMap[row].end(), point);
    
    if (it != rowIntersectionMap[row].end()){
        index = it - rowIntersectionMap[row].begin();
    }
    else{
        std::cout << "Element not found in row: " << point << std::endl;
        return false;
    }


    // determine the direction of search and update the point reference
    if(index % 2 == 0){
        point = rowIntersectionMap[row][index+1];
    }
    else{
        point = rowIntersectionMap[row][index-1];
    }

    return true;

}


/*
Get the next point up the contour
*/
bool Family::getNextPoint(Point& point){
    
    int contour_index;
    int index;

    // find the contour with the point
    for(int c = 0; c < contours.size(); c++){

        index = contours[c].findIntersectionPointIndex(point);

        if(index != -1){
            contour_index = c;
            break;
        }
    }

    Contour contour = contours[contour_index];

    Point prev = *contour.getIntersectionPoint(index-1);
    Point next = *contour.getIntersectionPoint(index+1);

    if((prev.y > point.y) && (next.y > point.y)){
        // remove the change of peaks
        return false;
    }
    else if(prev.available && prev.y > point.y){
        point = prev;
        return true;
    }
    else if(next.available && next.y > point.y){
        point = next;
        return true;
    }
    else{
        return false;
    }
    
}


/*
Return one path of the family
*/
std::vector<Point> Family::generatePath(Point startPoint){

    std::vector<Point> path;
    bool next_point = false;

    int row = startPoint.y;
    int index;

    Point point(startPoint.x, startPoint.y);

    // loop until there are no valid next points
    do{
        std::cout << point << std::endl;
        
        path.push_back(point);
        point.available = false;
        getAcrossPoint(point);

        std::cout << point << std::endl;

        path.push_back(point);
        point.available = false;
        next_point = getNextPoint(point);
        
    }while(next_point);

    return path;
}

std::vector<std::vector<Point>> Family::generateTotalPath(double lineThickness, Angle& angle){
    std::cout << "PATH GENERATION START" << std::endl;
    std::cout << "\tLINE THICKNESS " << lineThickness << std::endl;
    std::cout << "\tLINE ANGLE     " << angle << std::endl;


    std::vector<std::vector<Point>> total_path;
    
    // create the intersection points
    generateIntersectionPoints(lineThickness, angle);

    // get the starting point
    Point* startingPointer = getAvailablePoint();
    
    // loop until there are no starting points available
    
    while(startingPointer){

        generatePath(*startingPointer);

        std::cout << "HAHAHA" << std::endl;
        // get a new starting point (that has not been visited)
        startingPointer = getAvailablePoint();

        std::cout << "HOHOHO" << std::endl;

    }

    delete startingPointer;

    // return total_path

    return total_path;

}

std::ostream& operator<<(std::ostream &strm, const Family &f){
    return strm << "FAMILY NOT DONE";
}
