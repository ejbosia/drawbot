
#include "contour_fill_strategy.h"


ContourFillStrategy::ContourFillStrategy(double lineThickness):lineThickness(lineThickness){

}

std::vector<Contour> ContourFillStrategy::distanceTransform(Contour contour, double distance){
    // perform the distance transform

    std::vector<Point> transform_points;

    Angle previous, next, bisect;

    double hypothenus, dx, dy;

    Point p, pp, np;

    for(int i = 0; i < contour.size(); i++){

        pp = contour.get(i-1);
        np = contour.get(i+1);

        previous = contour.get(i).angle(pp);
        next = contour.get(i).angle(np);

        bisect.setAngle((next.getAngle()-previous.getAngle())/2);

        hypothenus = distance / bisect.sine();

        // rotate bisect to match previous
        bisect.rotateAngle(previous.getAngle());

        p = contour.get(i);
        p.translate(hypothenus, bisect);

        transform_points.push_back(p);

    }


    // clean up the contour
    std::vector<Contour> sub_contours;

    return sub_contours;
}

std::vector<std::vector<Point>> ContourFillStrategy::generateTotalPath(Family family){
    std::vector<std::vector<Point>> total_path;

    return total_path;
}


