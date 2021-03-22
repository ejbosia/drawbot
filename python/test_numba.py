import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from collections import Counter
import cv2
import convert_polygons as cp

from numba import jit

import shapely.affinity as sa
from shapely.geometry import Polygon, LineString, Point, MultiLineString




# find peaks numba
@jit(nopython=True)
def find_peaks_numba(contour):

    peaks = []
    
    end = len(contour)-1
    
    # check first point
    if contour[1][1] == contour[end][1]:
        peaks.append(contour[0])
    
    # check last point
    if contour[0][1] == contour[end-1][1]:
        peaks.append(contour[end])
    
    # check every point for peaks
    for i in range(1, end):
        if contour[i-1][1] == contour[i+1][1]:
            peaks.append(contour[i])
        
    return peaks



def generate_intersection_points(polygon, distance):

    l1 = LineString(list(polygon.envelope.exterior.coords)[0:2])
    l1 = l1.parallel_offset(0.5*distance, 'left')

    test = MultiLineString([polygon.exterior]+list(polygon.interiors))

    vertex_list = [p for p in polygon.exterior.coords]

    for interior in polygon.interiors:
        vertex_list.extend([p for p in interior.coords])

    contour_list = []

    for _ in range(len(test)):
        contour_list.append([])
        
    while l1.intersects(polygon):
        
        for i, x in enumerate(test):
            if l1.intersects(x):
                
                values = x.intersection(l1)
                
                ip = list(values)
                
                contour_list[i].extend(ip)    
            
        l1 = l1.parallel_offset(distance, 'left')


    # sort the contour points
    for i in range(len(contour_list)):
        
        # sort the points by the projection distance
        contour_list[i].sort(key = test[i].project)
        
    # sort the contour points
    for i in range(len(contour_list)):
        
        contour_list[i] = [(p.x,p.y) for p in contour_list[i]]



    # sort the contour points
    for i in range(len(contour_list)):
                
        # find the peaks in the contour
        peaks = find_peaks_numba(np.array(contour_list[i]))
        
        x = len(contour_list[i])

        # remove the peaks from the contour and intersection list
        for p in peaks:
                    
            contour_list[i].remove(tuple(p))

        print(x, len(contour_list[i]))
    
    input("WAIT")

    return contour_list



def plot_path(path):
    
    X = []
    Y = []
    
    
    if type(path[0]) == tuple or type(path[0]) == np.ndarray:
        
        for p in list(path):
            X.append(p[0])
            Y.append(p[1])

        plt.plot(X,Y)
    else:

        for p in list(path):
            X.append(p.x)
            Y.append(p.y)

        plt.plot(X,Y)

@jit(nopython=True) 
def next_point(point, contour_indices, all_points):
        
    i1 = np.where((all_points[:,0] == point[0]) & (all_points[:,1]==point[1]))[0][0]
    
    i0 = i1-1
    i2 = i1+1    
    
    if i0 in contour_indices:
        o = i0
        i0 = contour_indices[np.where(i0 == contour_indices)[0][0]+1] -1
        # print("\t i0:",o,i0)
    elif i2 in contour_indices:
        o=i2
        i2 = contour_indices[np.where(i2 == contour_indices)[0][0]-1]
        # print("\t i2:",o,i2)

        
    # check the previous point
    if all_points[i0][1] > point[1]:

        return all_points[i0]
    
    # check the next point
    if all_points[i2][1] > point[1]:
        
        return all_points[i2]    
    
    # if neither point returns
    return None


@jit(nopython=True) 
def across_point(point, all_points): 
        
    row = all_points[all_points[:,1]==point[1]][:,0]

    row.sort()


    if len(row) % 2 == 1:
        print(row)


    index = np.where((row == point[0]))[0][0]
        
    if index % 2 == 0:
        return np.array([row[index+1], point[1]])
    else:
        return np.array([row[index-1], point[1]])
    
    
# find a point not in the path
@jit(nopython=True)
def get_available_pt_index(last_start,total_path, all_points):
        
    for i in range(last_start, len(all_points)):
        if ((total_path[:,0] == all_points[i,0]) & (total_path[:,1] == all_points[i,1])).any():
            continue
        else:
            return i
    
    return -1   
    
@jit(nopython=True)
def numba_mode(index, all_points, contour_indices):    
    p1 = all_points[index]
    
    path = []
    
    while not p1 is None:
        
        if p1[0] > 3000:
            print("P1:", p1)

        path.append(p1)
        p2 = across_point(p1, all_points)

        if p2[0] > 3000:
            print("P2:", p2)

        path.append(p2)
        p1 = next_point(p2, contour_indices, all_points)    
        
        
    
    return path
    

def fill_path_numba(all_points, contour_indices):
    
    total_path = []
    temp = np.empty([0,2])
    start_index = 0
    
    print(temp.shape)

    sort_points = all_points[all_points[:,1].argsort()]
        
    last_start = 0
    
    while last_start != -1:

        print(start_index, all_points.shape, contour_indices[0])
        path = numba_mode(start_index, all_points, contour_indices)

        temp = np.append(temp, np.array(path), axis=0)
                        
        last_start = get_available_pt_index(last_start, temp, sort_points)
                
        if last_start != -1:
            start_point = sort_points[last_start]

            # get the start index in all points
            start_index = np.where((all_points[:,0]==start_point[0]) & (all_points[:,1]==start_point[1]))[0][0]

        total_path.append(path)

    return total_path

def main():
    image = cv2.imread("../images/test_pic.png", 0)
    c,h = cv2.findContours(image, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    p_list = cp.execute(image)
    polygon = p_list[-1]

    polygon = sa.rotate(polygon,np.pi/6, use_radians=True)

    distance = image.shape[0] * 0.001

    contour_list = generate_intersection_points(polygon, distance)

    all_points = []
        
    contour_indices = [0]

    sum = 0
    for contour in contour_list:
        sum+= len(contour)
        contour_indices.append(sum)
        
        for c in contour:
            all_points.append(c)
    #     plot_path(contour)

    # plt.show()


    result = fill_path_numba(np.array(all_points), np.array(contour_indices))

    pts = 0
    for path in result:
        plot_path(list(path))
        pts += len(path)
    plt.show()


if __name__ == "__main__":
    main()