
#include <iostream>
#include <chrono>

#include "point.h"

using namespace std;



void run(){

    cout << "Process Start" << endl;

    // create a point
    Point point(100, 100);

    cout << point.getX() << endl;
    cout << point.getY() << endl;

    string x = point.toString();

    cout << x;

}



int main(int argc, char** argv){

    auto start = chrono::high_resolution_clock::now();

    run();

    auto stop = chrono::high_resolution_clock::now(); 

    auto duration = chrono::duration_cast<chrono::microseconds>(stop - start); 
    
    cout << "TIME: " << duration.count() << " MICROSECONDS" << endl;    
    
    return 0;
}

