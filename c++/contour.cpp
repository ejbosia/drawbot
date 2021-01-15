#include "contour.h"
        
Contour::Contour(vector<Point>& vertexRef):vertexList(vertexRef){

}

/*
Get the vertex at the input index - loop around the vertex
*/
Point Contour::get(int index){
    return vertexList[index % vertexList.size()];
}

/*
Get the number of vertices in the contour
*/
int Contour::size(){
    return vertexList.size();
}



/*
Rotate all of the points in the contour about pt 0,0
*/
void Contour::rotate(Angle& angle){
    for(int i = 0; i < vertexList.size(); i++){
        vertexList[i].rotate(angle);
    }
}


/*
Find the index of the point before the input point - return -1 if not found
*/
int Contour::getStartingIndex(Point& p){

    int endIndex;

    for(int i = 0; i < vertexList.size(); i++){
        
        if(i+1 >= vertexList.size()){
            endIndex = 0;
        }
        else{
            endIndex = i+1;
        }

        // bring the next point to 0 ( to compare )
        Point next = vertexList[endIndex] - vertexList[i];
        
        // bring the test point to 0
        Point current = p - vertexList[i];

        DEBUG_MSG_C((current.y/current.x) << " == " << (next.y/next.x));

        // compare the ratio of y/x
        if((current.y/current.x) == (next.y/next.x)){
            return i;
        }
    }

    return -1;

}


/*
Find a point a distance around the perimeter of the contour
*/
Point* Contour::traverse(Point& start, double distance, bool clockwise){

    double length;

    int index = getStartingIndex(start);

    // set the direction
    int direction;
    if(clockwise){
        direction = 1;
        index += 1;
    }else{
        direction = -1;
    }

    double edgeDistance;

    while(distance > 0){

        edgeDistance = start.distance(vertexList[index]);

        std::cout << "\tSTART: " << start << " DISTANCE: " << distance << std::endl;
        
        // if the distance remaining is longer than the edge distance, move to the next edge
        if(distance > edgeDistance){

            // remove the edge distance from the distance remaining
            distance -= edgeDistance;

            // move the start point to the end of the current edge
            start = vertexList[index];

            // move to the next edge
            index = (index + direction) % vertexList.size();
        }

        // move the distance away from the current start point
        else{
            Angle a = start.angle(vertexList[index]);

            // translate the point in the direction of the end point the remaining distance
            Point* temp = new Point(start.x, start.y);
            
            (*temp).translate(distance, a);
            // return the point
            return temp;
        }

    }
    return NULL;
}


int Contour::findIntersectionPointIndex(Point& p){

    auto it = std::find(intersectionPoints.begin(), intersectionPoints.end(), p);;

    if(it != intersectionPoints.end()){
        return it - intersectionPoints.begin();
    }
    else{
        return -1;
    }

}

Point* Contour::getIntersectionPoint(int index){

    // loop index if necessary because contour is a loop
    index = index % intersectionPoints.size();

    return &intersectionPoints[index];
}

int Contour::getFirstAvailable(){

    for(int i = 0; i < intersectionPoints.size(); i++){
        if(intersectionPoints[i].available){
            return i;
        }
    }

    return -1;
}



// get the maximum point in the contour in the direction of the angle
Point Contour::getMaximumPoint(Angle& angle){

    Point maxPoint = vertexList.front();
    double maxValue = maxPoint.xRotation(angle);

    double tempValue;

    for(int i = 0; i < vertexList.size(); i++){
        
        tempValue = vertexList[i].xRotation(angle);
        DEBUG_MSG_C("TEMP: " << tempValue << "\t" << vertexList[i]);
        if(tempValue > maxValue){
            maxValue = tempValue;
            maxPoint = vertexList[i];
        }

    }

    DEBUG_MSG_C("ANGLE: " << angle.degrees() << "\tCOS: " << angle.cosine() << "\tSIN: " << angle.sine());
    return maxPoint;

}


ostream& operator<<(ostream &strm, const Contour &c){
    
    strm << "\nCONTOUR" << endl;

    for(int i = 0; i < c.vertexList.size(); i++){
        strm << "\t" << c.vertexList[i] << endl;
    }

    return strm;
}