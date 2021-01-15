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
Point* Family::getAcrossPoint(Point* point){

    int row = (int)point->y;
    int index;

    // find the index of the point
    std::vector<Point>::iterator it = find(rowIntersectionMap[row].begin(), rowIntersectionMap[row].end(), *point);
    
    if (it != rowIntersectionMap[row].end()){
        index = it - rowIntersectionMap[row].begin();
    }
    else{
        std::cout << "Element not found in row: " << point << std::endl;
        return NULL;
    }

    // std::cout << "\t" << point << " " << point->available << std::endl;

    // determine the direction of search and update the point reference
    if(index % 2 == 0){
        point = &(rowIntersectionMap[row][index+1]);
    }
    else{
        point = &(rowIntersectionMap[row][index-1]);
    }

    return point;

}


/*
Get the next point up the contour
*/
Point* Family::getNextPoint(Point* point, Point* start){
    
    int contour_index;
    int index;

    // find the contour with the point
    for(int c = 0; c < contours.size(); c++){

        index = contours[c].findIntersectionPointIndex(*point);

        if(index != -1){
            contour_index = c;
            break;
        }
    }
    // std::cout << "GNP: " << point << "\t" << point->available << std::endl;
    // std::cout << "GNPS: " << start << "\t" << start->available << std::endl;

    // std::cout << "GNPS: " << start << "\t" << start->available << std::endl;

    Point* prev = contours[contour_index].getIntersectionPoint(index-1);
    // std::cout << "GNPS: " << start << "\t" << start->available << std::endl;

    Point* next = contours[contour_index].getIntersectionPoint(index+1);
    // std::cout << "GNPS: " << start << "\t" << start->available << std::endl;

    // std::cout << "GNP: " << prev << "\t" << next << std::endl;
    // std::cout << "GNPS: " << start << "\t" << start->available << std::endl;

    Point temp(-1,-1);
    if((prev->y > point->y) && (next->y > point->y)){
        // remove the change of peaks
        return NULL;
    }
    else if(prev->available && prev->y > point->y){
        temp = *prev;
    }
    else if(next->available && next->y > point->y){
        temp = *next;
    }
    else{
        return NULL;
    }
    // std::cout << "GNP: " << point << "\t" << point->available << std::endl;
    // std::cout << "GNPS: " << start << "\t" << start->available << std::endl;


    // find temp in the map 
    for(int i = 0; i < rowIntersectionMap[(int)temp.y].size(); i++){
        if(temp == rowIntersectionMap[(int)temp.y][i]){
            // std::cout << "GNP: " << point << "\t" << point->available << std::endl;
            // std::cout << "GNPS: " << start << "\t" << start->available << std::endl;

            return &(rowIntersectionMap[(int)temp.y][i]);
        }
    }

    return NULL;

}


/*
Return one path of the family
*/
std::vector<Point> Family::generatePath(Point* point){

    std::vector<Point> path;
    bool next_point = false;

    Point* start = point;
    std::cout << *start << " " << start->available << std::endl;

    // loop until there are no valid next points
    do{
        // std::cout << point->available << std::endl;
        
        path.push_back(*point);
        (*point).available = false;
        // std::cout << "\t" << *point << " " << point << " " << point->available << std::endl;
        // std::cout << start << "\t" << start->available << std::endl;

        // update the pointer
        point = getAcrossPoint(point);
        std::cout << "ACROSS " << *point << " " << start << "\t" << start->available << std::endl;

        // std::cout << *point << std::endl;

        path.push_back(*point);
        (*point).available = false;
        // std::cout << "\t" << *point << " " << point << " " << point->available << std::endl;
        // std::cout << start << "\t" << start->available << std::endl;
        point = getNextPoint(point, start);
       
        std::cout << "NEXT "<< *point << " " << start << "\t" << start->available << std::endl;

    // }while(false);
    }while(point);

    std::cout << start << "\t" << start->available << std::endl;


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

        generatePath(startingPointer);

        // get a new starting point (that has not been visited)
        startingPointer = getAvailablePoint();


        for(Point p : rowIntersectionMap[0]){
            std::cout << p.available << " ";
        }

    }

    delete startingPointer;

    // return total_path

    return total_path;

}

std::ostream& operator<<(std::ostream &strm, const Family &f){
    return strm << "FAMILY NOT DONE";
}
