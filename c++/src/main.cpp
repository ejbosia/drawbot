
#include <iostream>
#include <chrono>
#include <fstream>
#include <vector>

#include "point.h"
#include "angle.h"
#include "line.h"
#include "contour.h"
#include "family.h"
#include "intersection_strategy.h"
#include "fill_strategy.h"
#include "linear_fill_strategy.h"
#include "gcode.h"

#include <stdio.h>
// #include <opencv2/core.hpp>
// #include <opencv2/imgcodecs.hpp>
// #include <opencv2/highgui.hpp>
#include <opencv2/opencv.hpp>


#define X_OFFSET 20.0
#define Y_OFFSET 20.0


using namespace std;


/*
Convert a contour into the Contour class
*/
Contour convertContour(vector<cv::Point> pointList, double scale_x, double scale_y){

    vector<Point> vertexList;

    for(int i = 0; i < pointList.size(); i++){
        
        cv::Point cv_pt = pointList[i];
        
        Point p(cv_pt.x * scale_x, cv_pt.y * scale_y);
 
        vertexList.push_back(p);
    }

    return Contour(vertexList);
}

int main(int argc, char** argv){

    std::cout.precision(std::numeric_limits<double>::digits10 + 2);

    auto start = chrono::high_resolution_clock::now();

    string image_path = "test_pic.png";
    std::cout << "IMAGE SLICER BEGIN" << std::endl;

    cv::Mat image = cv::imread(image_path, cv::IMREAD_GRAYSCALE);

    if(image.empty())
    {
        cout << "Could not read the image: " << image_path << endl;
        return 1;
    }

    // set the scale
    double scale_y = 100.0/((double)image.rows);
    double scale_x = 100.0/((double)image.cols);

    double scale;

    if(scale_x < scale_y){
        scale = scale_x;
    }else{
        scale = scale_y;
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

            vector<Contour> contourList;

            // create a family with the starting contour
            contourList.push_back(convertContour(contours[i], scale, scale));
            
            // add the children to the family

            int index = hierarchy[i][2];

            while(index != -1){
                
                contourList.push_back(convertContour(contours[index], scale, scale));

                index = hierarchy[index][0];

            }

            // add the family to the family list
            Family temp(contourList);

            familyList.push_back(temp);
        }
    }

    FillStrategy* strategy = new LinearFillStrategy(0.5, M_PI/6);

    vector<vector<Point>> total_path;

    for(Family family : familyList){
        for(vector<Point> path : strategy->generateTotalPath(family)){
            total_path.push_back(path);
        }
    }

    // cout << total_path.size() << endl;

    // cout << "X = [";
    // for(vector<Point> path : total_path){
    //     cout << "[";
    //     for(Point p : path){
    //         cout << p.x << ", ";
    //     }
    //     cout << "],";
    // }
    // cout << "]" << endl;

    // cout << "Y = [";
    // for(vector<Point> path : total_path){
    //     cout << "[";
    //     for(Point p : path){
    //         cout << p.y << ", ";
    //     }
    //     cout << "],";
    // }
    // cout << "]" << endl;

    // generate the gcode
    GCode gcode(X_OFFSET, Y_OFFSET);

    std::string output = gcode.generateGCode(total_path);

    std::ofstream out("output.gcode");
    out << output;

    auto stop = chrono::high_resolution_clock::now(); 

    auto duration = chrono::duration_cast<chrono::microseconds>(stop - start); 
    
    cout << "TIME: " << duration.count() << " MICROSECONDS" << endl;    
    
    return 0;
}

