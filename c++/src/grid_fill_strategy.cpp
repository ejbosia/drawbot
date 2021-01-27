
#include "grid_fill_strategy.h"



GridFillStrategy::GridFillStrategy(double lineThickness, Angle angle):lineThickness(lineThickness), angle(angle){
    intersectionStrategy = new HorizontalIntersectionStrategy(lineThickness);


}


std::vector<std::vector<Point>> GridFillStrategy::generateTotalPath(Family family){

    std::vector<std::vector<Point>> total_path;

    Angle reverse(-angle.getAngle());

    // rotate the family to match the angle
    family.rotate(reverse);

    // find the intersection points for each contour
    for(int i = 0; i < family.size(); i++){
        intersectionPoints.push_back(intersectionStrategy->generateIntersectionPoints(family.get(i)));
    }

}



