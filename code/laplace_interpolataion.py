from user_inputs import classified_ptcld_dir, in_file_ptcld_for_laplace, left, right, bottom, top, grid_resolution
from user_inputs import classified_ptcld_dir, DTM_dir
import laspy
import startinpy
import numpy as np

xc = np.arange(left, right, grid_resolution)
yc = np.arange(bottom, top, grid_resolution)
xc_co, yc_co = np.meshgrid(xc, yc)
grid_coordinates = np.c_[np.ravel(xc_co), np.ravel(yc_co)]

with laspy.open(classified_ptcld_dir + in_file_ptcld_for_laplace) as f:
    pt_cloud = f.read()
    classif = pt_cloud.classification.copy()
    ground_mask = classif == 2
    points_copy = pt_cloud.points
    ground_points = points_copy[ground_mask]
    x = ground_points.x.copy()
    y = ground_points.y.copy()
    z = ground_points.z.copy()
    xyz = np.vstack((x, y, z)).transpose()

# print(xyz.shape)


dt = startinpy.DT()
dt.read_las(classified_ptcld_dir + in_file_ptcld_for_laplace, classification=[2])

z_values = []
count = 0
for pt in grid_coordinates:
    try:
        z_values.append(dt.interpolate_laplace(pt[0], pt[1]))
    except:
        z_values.append(-9999)
        count += 1
print(count)
grid_resampled = np.c_[grid_coordinates, z_values]
np.savetxt(DTM_dir+in_file_ptcld_for_laplace[:-4]+"_resampled_laplace_grid"+".txt", grid_resampled, delimiter=',')
