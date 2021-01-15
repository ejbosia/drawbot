
#include "fill_strategy.h"


LinearFillStrategy::LinearFillStrategy(double lineThickness, Angle angle):lineThickness(lineThickness), angle(angle){
    intersectionStrategy = new HorizontalIntersectionStrategy(lineThickness);
}


bool comparePointPtr(Point* a, Point* b){
    return ((*a).x < (*b).x);
}


/*
Create the row intersection map
*/
void LinearFillStrategy::initRowIntersectionMap(){
    Point temp(0.0,0.0);

    // initialize the rowIntersectionPoints
    for(int i = 0; i < intersectionPoints.size(); i++){
        for(int j = 0; j < intersectionPoints[i].size(); i++){
            
            temp = intersectionPoints[i][j];
            
            // if the key does not exist, init an empty vector
            if(rowIntersectionMap.find((int)temp.y) == rowIntersectionMap.end()){
                rowIntersectionMap.insert(std::pair<int, std::vector<Point*>>((int)temp.y, std::vector<Point*>()));
            }

            // add the point coordinates to the map
            rowIntersectionMap[(int)temp.y].push_back(&intersectionPoints[i][j]);
        }
    }

    // sort each row of pointers
    for(std::map<int,std::vector<Point*>>::iterator it = rowIntersectionMap.begin(); it != rowIntersectionMap.end(); ++it)
    {
        std::sort(it->second.begin(), it->second.end()); // string's value 
        std::cout << "\tROW: " << it->first << ": ";
        for(Point* p : it->second){
            std::cout << *p << " ";
        }
        std::cout << std::endl;
    }
}


/*
Update the current index values to the point across the contour
*/
void LinearFillStrategy::getAcrossPoint(int& contour, int& index){
    
    Point* currentPtr = &intersectionPoints[contour][index];

    // make a temp array
    std::vector<Point*> rowPoints = rowIntersectionMap[(int)currentPtr->y];
    
    // find the pointer in the row points
    std::vector<Point*>::iterator it = std::find (rowPoints.begin(), rowPoints.end(), currentPtr); 

    if(it == rowPoints.end()){
        cout << "NOT FOUND!" << endl;
        throw 5;
    }

    index = it - rowPoints.begin();

    Point* newPtr;

    if(index % 2 == 0){
        newPtr = rowPoints[index+1];
    }
    else{
        newPtr = rowPoints[index-1];
    }

    findPoint(newPtr, contour, index);
}


/*
Get the next point around the contour. The point will always be "up" the contour in the Y direction
*/
void LinearFillStrategy::getNextPoint(int& contour, int& index){

    int cs = intersectionPoints[contour].size();

    double previous_y = intersectionPoints[contour][(index-1)%cs].y;
    double current_y = intersectionPoints[contour][index].y;
    double next_y = intersectionPoints[contour][(index+1)%cs].y;

    bool check_previous = (previous_y > current_y);
    bool check_next = (next_y > current_y);

    if(check_previous == check_next){
        contour = -1;
        index = -1;
    }
    else if(check_previous){
        index = (index-1)%cs;
    }
    else if(check_next){
        index = (index+1)%cs;
    }
}


/*
Get the first available point ~ lowest row, farthest left
*/
void LinearFillStrategy::getAvailablePoint(int& contour, int& index){

    std::vector<int> rowPts;

    // row points
    for(std::map<int,std::vector<Point*>>::iterator it = rowIntersectionMap.begin(); it != rowIntersectionMap.end(); ++it) {
        rowPts.push_back(it->first);
    }

    // sort the rows
    std::sort(rowPts.begin(), rowPts.end());

    // iterate through each row, and check each point right to left
    for(int row : rowPts){
        std::cout << "\t" << row << std::endl;
        for(Point* ptr : rowIntersectionMap[row]){
            if(ptr->available){
                findPoint(ptr, contour, index);
                return;
            }
        }
    }

    // if no point is found, set contour and index to -1
    contour = -1;
    index = -1;
}

// pick the lowest, farthest right point
void LinearFillStrategy::findPoint(Point* newPtr, int& contour, int& index){

    // find the contour, index position of the new point
    for (int c = 0; c < intersectionPoints.size(); c++) {

        std::vector<Point> contourVector = intersectionPoints[c];

        auto it = std::find(contourVector.begin(), contourVector.end(), *newPtr);
        
        // if the point is found, return the coordinates
        if (it != contourVector.end()) {
            contour = c;
            index = it - contourVector.begin();
        }
    }

    // if the point is not found, set contour and index to -1
    contour = -1;
    index = -1;
}


/*
Generate a path, moving back and forth
*/
std::vector<Point> LinearFillStrategy::generatePath(int& contour, int& index){
    
    std::vector<Point> path;

    // loop until there are no valid next points
    do{
        
        path.push_back(intersectionPoints[contour][index]);
        intersectionPoints[contour][index].available = false;
        getAcrossPoint(contour, index);


        path.push_back(intersectionPoints[contour][index]);
        intersectionPoints[contour][index].available = false;
        getNextPoint(contour, index);
       
    }while(contour != -1);

    return path;
}


/*
Generate a complete path for the family
*/
std::vector<std::vector<Point>> LinearFillStrategy::generateTotalPath(Family family){

    std::vector<std::vector<Point>> total_path;

    Angle reverse(-angle.getAngle());

    // rotate the family to match the angle
    family.rotate(reverse);

    // find the intersection points for each contour
    for(int i = 0; i < family.size(); i++){
        intersectionPoints.push_back(intersectionStrategy->generateIntersectionPoints(family.get(i)));
    }

    // std::cout << "x = [";

    // for(Point p : intersectionPoints[0]){
    //     std::cout << p.x << ", ";
    // }

    // std::cout << "]" << std::endl;

    // std::cout << "y = [";

    // for(Point p : intersectionPoints[0]){
    //     std::cout << p.y << ", ";
    // }
    
    // std::cout << "]" << std::endl;

    // index of point in the two vector storage
    int contour = 0;
    int index = 0;

    getAvailablePoint(contour, index);

    while(contour != -1){

        total_path.push_back(generatePath(contour, index));

        getAvailablePoint(contour, index);
    }

    // clear the state variables of the fill strategy
    intersectionPoints.clear();
    rowIntersectionMap.clear();

    // rotate all of the points back to the original orientation
    for(std::vector<Point> path : total_path){
        for(Point p : path){
            p.rotate(angle);
        }
    }
    
    family.rotate(angle);

    return total_path;
}