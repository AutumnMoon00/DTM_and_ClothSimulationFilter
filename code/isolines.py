##this can all be defined in a function
import numpy as np
import startinpy
from functions import distance, ratio, point_on_line
from user_inputs import fname_iso, ci, contour_start, contour_end

##loading file and creating DT
arr = np.loadtxt(fname=fname_iso,dtype="float", delimiter=',')
arr_list = arr.tolist()
dt = startinpy.DT()
dt.insert(arr_list)
##
contour_level = ci
trs = dt.triangles


contour_lines = []
for i in range(contour_start, contour_end+1, contour_level):

    for tri in trs:

        fv = tri[0]
        sv = tri[1]
        tv = tri[2]
        fv_xyz = dt.get_point(fv)
        sv_xyz = dt.get_point(sv)
        tv_xyz = dt.get_point(tv)
        points = []
        if max(fv_xyz[2], sv_xyz[2], tv_xyz[2]) > 1000:
                continue
        if (fv_xyz[2] <= i <= sv_xyz[2]) or (sv_xyz[2] <= i <= fv_xyz[2]): # 1-2 and 2-1
            length = distance(fv_xyz[0],fv_xyz[1],sv_xyz[0],sv_xyz[1])
            r = ratio(fv_xyz[2],sv_xyz[2],i)
            place_of_point = point_on_line(r, fv_xyz[0], fv_xyz[1], sv_xyz[0], sv_xyz[1])
            points.append(place_of_point)
        if (fv_xyz[2] <= i <= tv_xyz[2]) or (tv_xyz[2] <= i <= fv_xyz[2]): # 1-3 and 3-1
            length = distance(fv_xyz[0],fv_xyz[1],tv_xyz[0],tv_xyz[1])
            r = ratio(fv_xyz[2],tv_xyz[2],i)
            place_of_point = point_on_line(r, fv_xyz[0],fv_xyz[1],tv_xyz[0],tv_xyz[1])
            points.append(place_of_point)
        if (sv_xyz[2] <= i <= tv_xyz[2]) or (tv_xyz[2] <= i <= sv_xyz[2]): # 2-3 and 3-2
            length = distance(sv_xyz[0],sv_xyz[1],tv_xyz[0],tv_xyz[1])
            r = ratio(sv_xyz[2],tv_xyz[2],i)
            place_of_point = point_on_line(r, sv_xyz[0],sv_xyz[1],tv_xyz[0],tv_xyz[1])
            points.append(place_of_point)

        points = list(set(points)) #to extract only unique vertices

        if len(points)>1:
            # print(points[0][0], points[0][1], "hi", points[1][0], points[1][1])
            # make a line string of the 2 points in points and appending that to contour_arrays along with contour value
            contour_lines.append([f"LINESTRING({points[0][0]} {points[0][1]}, {points[1][0]} {points[1][1]})", i])

## print(contour_lines)

with open('isolines_final.txt','w') as i1:
    i1.write("wkt; Z\n")
    for item in contour_lines:
        # print(item)
        i1.write(f"{item[0]}; {item[1]}\n")

