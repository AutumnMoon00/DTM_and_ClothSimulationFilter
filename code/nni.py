from user_inputs import cloth_out_dir, in_cloth_file_for_nni, left, right, bottom, top, grid_resolution, DTM_dir
import laspy
import startinpy
import numpy as np

xc = np.arange(left, right, grid_resolution)
yc = np.arange(bottom, top, grid_resolution)
xc_co, yc_co = np.meshgrid(xc, yc)
grid_coordinates = np.c_[np.ravel(xc_co), np.ravel(yc_co)]

dt = startinpy.DT()

# loading cloth file
cloth_data = np.loadtxt(cloth_out_dir+in_cloth_file_for_nni, delimiter=',')
list_of_cloth_pts = cloth_data.tolist()
dt.insert(list_of_cloth_pts)
print(dt)
z_values = []
for co in grid_coordinates:
    try:
        z_values.append(dt.interpolate_nni(co[0], co[1]))
    except:
        z_values.append(-9999)
grid_resampled = np.c_[grid_coordinates, z_values]
np.savetxt(DTM_dir+in_cloth_file_for_nni[:-4]+"_nni_resampled_grid"+".txt", grid_resampled, delimiter=',')
