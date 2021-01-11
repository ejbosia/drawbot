
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


    //std::cout.precision(std::numeric_limits<double>::digits10 + 2);

    auto start = chrono::high_resolution_clock::now();

    string image_path = "test2.png";

    cv::Mat image = cv::imread(image_path, cv::IMREAD_GRAYSCALE);

    if(image.empty())
    {
        cout << "Could not read the image: " << image_path << endl;
        return 1;
    }

    // get the contours
    vector<vector<cv::Point>> contours;
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

            familyList.push_back(temp);
        }
    }

    Angle a(M_PI/6);
    // Angle a(0);

    for(int i = 0; i < familyList.size(); i++){
        familyList[i].generateTotalPath(1, a);
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

