
#ifndef ANGLE_H
#define ANGLE_H

#include <iostream>
#include <string>

class Angle{

    private:
        double angle;
        

    public:
        Angle(double angle);

        // mutators and accessors
        double getAngle();
        void rotateAngle(double angle);
        void setAngle(double angle);


        // trig functions
        double sine();
        double cosine();
        double tangent();

        // operator overloads
        bool operator==(const Angle& other);
        friend std::ostream& operator<<(std::ostream &strm, const Angle &a);

};

#endif