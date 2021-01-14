#include <iostream>
#include <math.h>

using namespace std;

int main(){


    double a1,a2,a3;

    a1 = 0;
    a2 = M_PI/2-0.0001;
    a3 = M_PI/2;

    cout << tan(a1) << endl;
    cout << tan(a2) << endl;
    cout << tan(a3) << endl;

    return 0;
}