
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
    std::cout << "ROW INTERSECTION MAP" << std::endl;

    vector<int> rowPts;

    int row;
    // initialize the rowIntersectionPoints
    for(int i = 0; i < intersectionPoints.size(); i++){
        for(int j = 0; j < intersectionPoints[i].size(); j++){
            
            temp = intersectionPoints[i][j];

            row = std::round(temp.y/lineThickness);
            
            // if the key does not exist, init an empty vector
            if(rowIntersectionMap.find(row) == rowIntersectionMap.end()){
                rowIntersectionMap.insert(std::pair<int, std::vector<Point*>>(row, std::vector<Point*>()));
            }

            // add the point coordinates to the map
            rowIntersectionMap[row].push_back(&intersectionPoints[i][j]);

            if(std::find(rowPts.begin(), rowPts.end(), row) == rowPts.end()){
                rowPts.push_back(row);
            }
        }

        std::sort(rowPts.begin(), rowPts.end());

        for(int r : rowPts){

            if(rowIntersectionMap[r].size()){
                std::cout << "ROW" << r << " SIZE: " << rowIntersectionMap[r].size() << std::endl;
            }
        }
    }


    // sort each row of pointers by the x position
    for(std::map<int,std::vector<Point*>>::iterator it = rowIntersectionMap.begin(); it != rowIntersectionMap.end(); ++it)
    {
        std::sort((*it).second.begin(), (*it).second.end(),comparePointPtr);
    }
}


/*
Update the current index values to the point across the contour
*/
void LinearFillStrategy::getAcrossPoint(int& contour, int& index){

    // std::cout << "ACROSS " << contour << " " << index  <<std::endl;

    Point* currentPtr = &intersectionPoints[contour][index];
    // std::cout << "\t CURRENT " << *currentPtr << " " << currentPtr <<std::endl;

    int row = std::round(currentPtr->y/lineThickness);

    // std::cout << "\t SIZE: " <<rowIntersectionMap[row].size() << std::endl;
    // make a temp array
    std::vector<Point*> rowPoints = rowIntersectionMap[row];
    
    // find the pointer in the row points
    std::vector<Point*>::iterator it = std::find (rowPoints.begin(), rowPoints.end(), currentPtr); 

    if(it == rowPoints.end()){
        std::cout << "NOT FOUND! " << *currentPtr << " " << row << endl;

        // for(Point* p : rowPoints){
        //     std::cout << *p << " ";
        // }

        // std::cout << std::endl;

        // std::cout << contour << " " << index << std::endl;

        throw 5;
    }

    index = it - rowPoints.begin();

    Point* newPtr;

    if(index % 2 == 0){

        // std::cout << "MAX " << index+1 << std::endl;
        newPtr = rowPoints[index+1];
    }
    else{
        // std::cout << "ODD " << index-1 << std::endl;
        newPtr = rowPoints[index-1];
    }

    findPoint(newPtr, contour, index);
}


/*
Get the next point around the contour. The point will always be "up" the contour in the Y direction
*/
void LinearFillStrategy::getNextPoint(int& contour, int& index){
    // std::cout << "NEXT " << contour << " " << index <<std::endl;

    int cs = intersectionPoints[contour].size();

    int low_index = (index-1);
    if(low_index < 0){
        low_index = cs-1;
    }
    
    int high_index = (index+1);
    if(high_index == cs){
        high_index = 0;
    }

    int previous_y = std::round(intersectionPoints[contour][low_index].y/lineThickness);
    int current_y = std::round(intersectionPoints[contour][index].y/lineThickness);
    int next_y = std::round(intersectionPoints[contour][high_index].y/lineThickness);

    bool check_previous = (previous_y > current_y) && intersectionPoints[contour][low_index].available;
    bool check_next = (next_y > current_y) && intersectionPoints[contour][high_index].available;

    if(check_previous == check_next){
        contour = -1;
        index = -1;
    }
    else if(check_previous){
        index = low_index;
    }
    else if(check_next){
        index = high_index;
    }
}


/*
Get the first available point ~ lowest row, farthest left
*/
void LinearFillStrategy::getAvailablePoint(int& contour, int& index){

    // std::cout << "AVAILABLE" << std::endl;

    std::vector<int> rowPts;

    // row points
    for(std::map<int,std::vector<Point*>>::iterator it = rowIntersectionMap.begin(); it != rowIntersectionMap.end(); ++it) {
        rowPts.push_back(it->first);
    }

    // sort the rows
    std::sort(rowPts.begin(), rowPts.end());


//     for(Point* ptr : rowIntersectionMap[-113]){
//         std::cout << *ptr << " ";
//     }
//     std::cout << std::endl;


//    // iterate through each row, and check each point right to left
//     for(Point* ptr : rowIntersectionMap[-114]){
//         std::cout << *ptr << " ";
//     }

//     std::cout << std::endl;

//     // iterate through each row, and check each point right to left
    for(int row : rowPts){

        for(Point* ptr : rowIntersectionMap[row]){
            // std::cout << ptr << " ";
            if(ptr->available){
                std::cout << "\t" << row << " " << *ptr << std::endl;
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
    // std::cout << "\tFIND: " << newPtr << std::endl;
    // find the contour, index position of the new point
    for (int c = 0; c < intersectionPoints.size(); c++) {

        std::vector<Point> contourVector = intersectionPoints[c];

        auto it = std::find(contourVector.begin(), contourVector.end(), *newPtr);
        
        // if the point is found, return the coordinates
        if (it != contourVector.end()) {
            contour = c;
            index = it - contourVector.begin();
            
            // std::cout << "FOUND " << contourVector[index] << " " <<intersectionPoints[contour][index] << std::endl;
            // std::cout << "\t" << newPtr << " " << &intersectionPoints[contour][index] << std::endl;

            return;
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

    // std::cout << intersectionPoints[contour][index] << "\t" << intersectionPoints[contour][index].available << " " << &intersectionPoints[contour][index] << std::endl;

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

    // generate the row intersection map
    initRowIntersectionMap();

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
    for(int c = 0; c < total_path.size(); c++){
        for(int i = 0; i < total_path[c].size(); i++){
            total_path[c][i].rotate(angle);
        }
    }
    
    family.rotate(angle);

    return total_path;
}


/*
GRID FILL

*/
