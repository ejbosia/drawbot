
#include <iostream>
#include <chrono>

#include <vector>

#include "point.h"
#include "angle.h"
#include "line.h"
#include "contour.h"
#include "family.h"


#include <stdio.h>
// #include <opencv2/core.hpp>
// #include <opencv2/imgcodecs.hpp>
// #include <opencv2/highgui.hpp>
#include <opencv2/opencv.hpp>


using namespace std;


/*
Convert a contour into the Contour class
*/
Contour convertContour(vector<cv::Point> pointList){

    vector<Point> vertexList;

    for(int i = 0; i < pointList.size(); i++){
        
        cv::Point cv_pt = pointList[i];
        
        Point p(cv_pt.x, cv_pt.y);
 
        vertexList.push_back(p);
    }

    return Contour(vertexList);
}

int main(int argc, char** argv){


    std::cout.precision(std::numeric_limits<double>::digits10 + 2);

    auto start = chrono::high_resolution_clock::now();

    vector<Point> square;
    
    square.push_back(Point(0,0));
    square.push_back(Point(0,10));
    square.push_back(Point(10,10));
    square.push_back(Point(10,0));

    Contour contour(square);

    Point test(5,0);

    cout << "STARTING INDEX (5,0): 0 == " << contour.getStartingIndex(test) << endl;

    test.x = 0;
    test.y = 5;

    cout << "STARTING INDEX (0,5): 3 == " << contour.getStartingIndex(test) << endl;

    cout << "\n\nTEST TRAVERSAL" << endl;
    double distance = 12.5;
    cout << "POINT: " << test << " DISTANCE: " << distance << " TRAVERSAL: \n" << *contour.traverse(test, distance) << endl;


    distance = 25;
    cout << "POINT: " << test << " DISTANCE: " << distance << " TRAVERSAL: \n" << *contour.traverse(test, distance) << endl;

    vector<Contour> children;

    Family family(contour, children);

    Angle angle(M_PI/6);

    family.generateTotalPath(1, angle);

    auto stop = chrono::high_resolution_clock::now(); 

    auto duration = chrono::duration_cast<chrono::microseconds>(stop - start); 
    
    cout << "TIME: " << duration.count() << " MICROSECONDS" << endl;    
    
    return 0;
}

