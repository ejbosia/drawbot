
#ifndef RAY_H
#define RAY_H

#include <iostream>
#include <string>

#include "point.h"
#include "angle.h"


class Ray{

    private:
        Point p1;
        Angle angle;

    public:
        Ray(Point& p, Angle& a);

        virtual Point getPoint();
        virtual Angle getAngle();

        // Point intersection(Ray& ray);
        // Point intersection(Line& line);

        friend std::ostream& operator<<(std::ostream &strm, const Ray &r);
};

#endif