# drawbot
This repository works with the "drawbot" project, which is a simple cartesian drawing robot. The program takes in binary images and "fills" them using different fill techniques. An eventual goal is to branch into more generic images, including color.

 - Python: code used to testing
 - C++: code used to improve performance

**It is still in progress**

Right now the goal is to convert to the Shapely library for python. Using an existing geometry processing library should help a lot with bugs in the intersection code.

## Fill Techniques
 - Rectilinear fill
 - Spiral fill
 - *CFS fill*

## Shading Techniques
 - *in progress*

## Drawing Techniques
 - *out-line trace*
 - *skeleton trace*
