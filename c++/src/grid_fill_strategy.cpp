
#include "grid_fill_strategy.h"



GridFillStrategy::GridFillStrategy(double lineThickness, Angle angle):lineThickness(lineThickness), angle(angle){
    intersectionStrategy = new HorizontalIntersectionStrategy(lineThickness);


}


std::vector<std::vector<Point>> generateTotalPath(Family family){

    std::vector<std::vector<Point>> total_path;




}



