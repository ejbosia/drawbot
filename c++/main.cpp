
#include <iostream>
#include <chrono>

#include <vector>

#include "point.h"
#include "angle.h"
#include "ray.h"
#include "line.h"
#include "contour.h"


using namespace std;


vector<Line> getTestLines(){

    double x,y;

    vector<Line> lineList;
    vector<Point> pointList;


    for(int i = 0; i < 4; i++){

        x = (double)(((i+1)/2)%2);
        y = (double)((i/2)%2);

        Point p(x,y);

        cout << "\t" << p << endl;
        
        pointList.push_back(p);
        
    }

    Point start = pointList.back();

    for(int i = 0; i < pointList.size(); i++){
        
        Point end = pointList[i];

        Line l(start, end);

        lineList.push_back(l);

        start = pointList[i];
    }

    return lineList;
}


void run(){

    cout << "Process Start" << endl;
    /*
    // create a point
    Point point(100, 100);

    cout << "POINT: " << point << endl;


    Angle angle(10);

    cout << "ANGLE: " << angle << endl;

    Ray ray(point, angle);

    cout << "RAY\n\t" << ray << endl;

    Point p2(200,200);

    Line line(point, p2);

    cout << "Line\n\t" << line << endl;
    */
    vector<Line> temp = getTestLines();

    Contour contour(temp);

    cout << contour << endl;

}


int main(int argc, char** argv){

    auto start = chrono::high_resolution_clock::now();

    run();

    auto stop = chrono::high_resolution_clock::now(); 

    auto duration = chrono::duration_cast<chrono::microseconds>(stop - start); 
    
    cout << "TIME: " << duration.count() << " MICROSECONDS" << endl;    
    
    return 0;
}

