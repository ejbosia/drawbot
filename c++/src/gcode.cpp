#include "gcode.h"

GCode::GCode(double x_offset, double y_offset): x_offset(x_offset), y_offset(y_offset){
    // Z_UP = "M106 S0;\nG4 P800;";
    // Z_DOWN = "M106 S255;\nG4 P800;";


    Z_UP = "G01 Z1;";
    Z_DOWN = "G01 Z10";
}


std::string GCode::commandDraw(double x, double y){
    return "G01 X" + std::to_string(x+x_offset) + " Y" + std::to_string(y+y_offset) + ";\n";
}


std::string GCode::commandDraw(Point p){
    return "G01 X" + std::to_string(p.x+x_offset) + " Y" + std::to_string(p.y+y_offset) + ";\n";
}


std::string GCode::commandTravel(double x, double y){
    return "G00 X" + std::to_string(x+x_offset) + " Y" + std::to_string(y+y_offset) + ";\n";
}


std::string GCode::commandTravel(Point p){
    return "G00 X" + std::to_string(p.x+x_offset) + " Y" + std::to_string(p.y+y_offset) + ";\n";
}


std::string GCode::commandUp(){
    return Z_UP + "\n";
}


std::string GCode::commandDown(){
    return Z_DOWN + "\n";
}


std::string GCode::generateSubPath(std::vector<Point> sub_path){

    // move to start position
    std::string sub_gcode = commandTravel(sub_path[0]);    

    // move the pen down
    sub_gcode += commandDown();

    // draw through each point
    for(int j = 1; j < sub_path.size(); j++){

        sub_gcode += commandDraw(sub_path[j]);

    }

    // move the pen up
    sub_gcode += commandUp();

    return sub_gcode;
}


std::string GCode::generateGCode(std::vector<std::vector<Point>> total_path){

    
    std::string output = "";

    // set the speeds
    output += "G00 F6000;\n";
    output += "G01 F2400;\n\n";

    // set the Z steps per mm
    // one rotation is "20 mm"
    output += "M92 Z10;\n\n";

    // home the start
    output += Z_UP + "\n";
    output += "G28 X Y;\n\n";

    // loop through each path
    for(int i = 0; i < total_path.size(); i++){
        output += generateSubPath(total_path[i]);
    }

    // home the XY axis
    output += "\nG28 X Y;\n\n";

    return output;
}