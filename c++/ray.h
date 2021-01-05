
#ifndef RAY_H
#define RAY_H

#include <iostream>
#include <string>

#include "point.h"
#include "angle.h"


class Ray{

    private:
        Point point;
        Angle angle;

    public:
        Ray(Point& p, Angle& a);

        friend std::ostream& operator<<(std::ostream &strm, const Ray &r);
};

#endif