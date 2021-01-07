
#include <iostream>
#include <chrono>

#include <vector>

#include "point.h"
#include "angle.h"
#include "ray.h"
#include "line.h"
#include "contour.h"
#include "family.h"


#include <stdio.h>
// #include <opencv2/core.hpp>
// #include <opencv2/imgcodecs.hpp>
// #include <opencv2/highgui.hpp>
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


void _test_single_intersection(Line l1, Line l2){
    Point* t1 =  l1.intersection(l2);
    Point* t2 =  l2.intersection(l1);

    if(t1)
        cout << "INTERSECTION TEST 1:\t" << *t1 << endl;
    else
        cout << "INTERSECTION TEST 1:\t NULL" << endl;
    if(t2)
        cout << "INTERSECTION TEST 2:\t" << *t2 << endl;
    else
        cout << "INTERSECTION TEST 2:\t NULL" << endl;

}


void _test_intersection(){
    cout << "\nTEST INTERSECTION" << endl;

    Point p1(0,0);
    Point p2(5,5);
    Point p3(5,0);
    Point p4(0,5);

    Line l1(p1,p2);
    Line l2(p3,p4);

    _test_single_intersection(l1, l2);

    Point p5(0,3);
    Point p6(5,3);
    
    Line l3(p5,p6);

    _test_single_intersection(l1, l3);


    Point p7(2,0);
    Point p8(2,5);
    
    Line l4(p7,p8);
    _test_single_intersection(l3, l4);

    Point p9(6,0);
    Point p10(6,10);
    
    Line l5(p9,p10);

    _test_single_intersection(l3, l5);


}

Contour convertContour(vector<cv::Point> pointList){

    vector<Line> lineList;

    cv::Point start = pointList.back();

    for(int i = 0; i < pointList.size(); i++){
        
        cv::Point end = pointList[i];
        
        Point p1(start.x, start.y);
        Point p2(end.x, end.y);

        Line l(p1, p2);
 
        lineList.push_back(l);

        start = pointList[i];
    }

    return Contour(lineList);
}


int main(int argc, char** argv){

    std::cout.precision(std::numeric_limits<double>::digits10 + 2);

    auto start = chrono::high_resolution_clock::now();

    
    string image_path = "picture.png";

    cv::Mat image = cv::imread(image_path, cv::IMREAD_GRAYSCALE);

    if(image.empty())
    {
        cout << "Could not read the image: " << image_path << endl;
        return 1;
    }


    // get the contours
    vector<vector<cv::Point> > contours;
    vector<cv::Vec4i> hierarchy;
    cv::findContours( image, contours, hierarchy, cv::RETR_CCOMP, cv::CHAIN_APPROX_SIMPLE );


    // create contour families
    vector<Family> familyList;

    for(int i = 0; i < contours.size(); i++){

        // check if the contour is a parent contour
        if(hierarchy[i][3]==-1){

            // create a contour of the parent
            cout << "PARENT " << hierarchy[i] << endl; 

            // create a family with the starting contour
            Contour parentContour = convertContour(contours[i]);
            
            // add the children to the family
            
            vector<Contour> childContourList;

            int index = hierarchy[i][2];

            while(index != -1){
                cout << "CHILD " << index << hierarchy[index] << endl; 

                childContourList.push_back(convertContour(contours[index]));

                index = hierarchy[index][0];

            }

            // add the family to the family list
            
            Family temp(parentContour, childContourList);

            cout << temp << endl;
            
            familyList.push_back(temp);

        }
    }
    
    //cv::imshow("Display window", image);
    //int k = cv::waitKey(0); // Wait for a keystroke in the window

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

