
#ifndef FAMILY_H
#define FAMILY_H

#if defined(DEBUG) || defined(DEBUG_FAMILY)
#define DEBUG_MSG(str) do { std::cout << "DEBUG FAMILY\t" << str << std::endl; } while( false )
#else
#define DEBUG_MSG(str) do { } while ( false )
#endif


#include <iostream>
#include <string>
#include <math.h>
#include <algorithm>
#include <vector>

#include "point.h"
#include "contour.h"

class Family{
    
    private:
        std::vector<Contour> contours;  // parent contour is the first contour

    public:
        Family(std::vector<Contour>& children);

        // Family contour-list accessor methods
        Contour get(int index);
        int size();

        void rotate(Angle& angle);

        friend std::ostream& operator<<(std::ostream &strm, const Family &f);
};

#endif