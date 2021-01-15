#include "intersection_strategy.h"


HorizontalIntersectionStrategy::HorizontalIntersectionStrategy(double lineThickness): lineThickness(lineThickness){}

/*
Find the intersection points using the horizontal line strategy
*/
std::vector<Point> HorizontalIntersectionStrategy::generateIntersectionPoints(Contour contour){

    std::vector<Point> intersectionPoints;

    // loop through the vertices
    for(int i = 0; i < contour.size(); i++){

        // get the start and end points
        Point start = contour.get(i);
        Point end = contour.get(i+1);

        // get the start and end y locations for looping
        // these locations are capped inwards on the line (end point capped by loop)

        // offset for the iteration process (moving the line to (0,0) does not make the intersection points on the integers)

        double dxdy = 1/start.angle(end).tangent(); // dx/dy slope of the line (inverse of usual)
        double x,y;

        double index;
        double distance = end.y - start.y;

        if(distance > 0){
            
            //index = interval-fmod(start.y, interval);
            index = lineThickness*ceil(start.y/lineThickness)-start.y;
            
            while(index <= distance){
                
                x = dxdy * index + start.x;
                y = index + start.y;

                index += lineThickness;

                intersectionPoints.push_back(Point(x,y));

            }
        }  
        else{

            index = lineThickness*floor(start.y/lineThickness)- start.y;
            
            while(index >= distance){

                x = dxdy * index + start.x;
                y = index + start.y;
                
                index -= lineThickness;

                intersectionPoints.push_back(Point(x,y));

            }
        }    
    }

    return intersectionPoints;
}
