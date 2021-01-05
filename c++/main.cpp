
#include <iostream>
#include <chrono>

#include "point.h"
#include "angle.h"
#include "ray.h"
#include "line.h"


using namespace std;



void run(){

    cout << "Process Start" << endl;

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

}



int main(int argc, char** argv){

    auto start = chrono::high_resolution_clock::now();

    run();

    auto stop = chrono::high_resolution_clock::now(); 

    auto duration = chrono::duration_cast<chrono::microseconds>(stop - start); 
    
    cout << "TIME: " << duration.count() << " MICROSECONDS" << endl;    
    
    return 0;
}

