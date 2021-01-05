#include "angle.h"

#include <math.h>


/*
Create an angle object. This enforces angles between 0-2PI
*/
Angle::Angle(double angle){
    setAngle(angle);
}

/*
Get the angle value of the object
*/
double Angle::getAngle(){
    return angle;
}

/*
Rotate the angle, maintain 0-2PI
*/
void Angle::rotateAngle(double angle){
    setAngle(this->angle + angle);
}

/*
Set the angle, maintain 0-2PI
*/
void Angle::setAngle(double angle){
    this->angle = std::fmod(angle,(2*M_PI));
}

double Angle::sine(){
    return sin(angle);
}

double Angle::cosine(){
    return cos(angle);
}

double Angle::tangent(){
    return tan(angle);
}

/*
OPERATER OVERLOADS
*/

/*
Check if angles are equivalent
*/
bool Angle::operator==(const Angle& other){
    return angle == other.angle;
}


/*
Output the angle
*/
std::ostream& operator<<(std::ostream &strm, const Angle &a) {
    return strm << a.angle << " Radians";
}


