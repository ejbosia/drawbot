#include "angle.h"

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

/*
Check if the input angle is parallel to the angle
*/
bool Angle::parallel(double a){
    return 0 == std::fmod(angle-a,(M_PI));
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

    // std::cout << "\t\t" << angle << std::endl;
    // std::cout << "\t\t" << other.angle << std::endl;
    // std::cout << "\t\t" << fabs(angle - other.angle);
    // std::cout << " ?< " << std::numeric_limits<double>::epsilon() << std::endl;
    

    return fabs(angle - other.angle) < std::numeric_limits<double>::epsilon();
}

/*
Check if angles are equivalent
*/
bool Angle::operator==(const double value){

    // std::cout << "\t" << angle << std::endl;
    // std::cout << "\t" << value << std::endl;

    // std::cout << "\t\t" << angle << std::endl;
    // std::cout << "\t\t" << value << std::endl;
    // std::cout << "\t\t" << fabs(angle - value);
    // std::cout << " ?< " << std::numeric_limits<double>::epsilon() << std::endl;

    return fabs(angle - value) < std::numeric_limits<double>::epsilon();
}


/*
Output the angle
*/
std::ostream& operator<<(std::ostream &strm, const Angle &a) {
    return strm << a.angle;
}


