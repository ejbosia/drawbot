
#include <iostream>
#include <chrono>

#include <vector>

#include "point.h"
#include "angle.h"
#include "ray.h"
#include "line.h"
#include "contour.h"


#include <stdio.h>
#include <opencv2/opencv.hpp>

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

void _test_contour(){

    cout << "\nTEST CONTOUR" << endl;

    vector<Line> temp = getTestLines();

    Contour contour(temp);

    cout << contour << endl;

}

void _test_distance(){

    cout << "\nTEST DISTANCE" << endl;

    Point p1(0,0);

    Point p2(3,4);

    cout << p2.distance(p1) << " == " << p1.distance(p2) << endl;

}

void _test_intersection(){
    cout << "\nTEST INTERSECTION" << endl;

    Point p1(0,0);
    Point p2(5,5);
    Point p3(5,0);
    Point p4(0,5);

    Line l1(p1,p2);
    Line l2(p3,p4);

    cout << *l1.intersection(l2) << endl;

    Point p5(0,3);
    Point p6(5,3);
    
    Line l3(p5,p6);

    cout << *l1.intersection(l3) << endl;
    cout << *l3.intersection(l1) << endl;

    Point p7(2,0);
    Point p8(2,5);
    
    Line l4(p7,p8);

    cout << *l3.intersection(l4) << endl;
    cout << *l4.intersection(l3) << endl;

}


int main(int argc, char** argv){

    auto start = chrono::high_resolution_clock::now();

    /*
    _test_contour();

    _test_distance();

    _test_intersection();
    */

    

    auto stop = chrono::high_resolution_clock::now(); 

    auto duration = chrono::duration_cast<chrono::microseconds>(stop - start); 
    
    cout << "TIME: " << duration.count() << " MICROSECONDS" << endl;    
    
    return 0;
}

