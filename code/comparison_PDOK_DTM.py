from user_inputs import DTM_dir, file_1, file_2
from functions import r_squared, rmse, nrmse, mutual_information
import numpy as np
import rasterio
import startinpy

# data loading
# f1 = rasterio.open(DTM_dir+file_1)
# f1 = f1.read(1)
# # print(f1)
# print(f1.shape)

with rasterio.open(DTM_dir+file_1) as src:
    # band1 = src.read(1)
    f1 = src.read(1)
    # print('Band1 has shape', f1.shape)
    height = f1.shape[0]
    width = f1.shape[1]
    cols, rows = np.meshgrid(np.arange(width), np.arange(height))
    xs, ys = rasterio.transform.xy(src.transform, rows, cols)
    lons = np.array(xs)
    lats = np.array(ys)

    # coordinates
    xc = lons.ravel(); yc = lats.ravel()
    z1 = f1.ravel()
    xyz1 = np.c_[xc, yc, z1]
    # print(xc.shape, yc.shape, z1.shape)
    # print('lons shape', lons.shape)
    pixels_with_values_idxs = xyz1[:, 2] != xyz1[:, 2].max()
    xyz2 = xyz1[pixels_with_values_idxs]
    # pdok pixel coordinates are not matching with resampled grid coordinates of our DTMs
    # so interpolating PDOK DTM to match our grid using laplace
    dt = startinpy.DT()
    dt.insert(xyz2.tolist())
    # print(xyz2.tolist())
print("done")
#
f2 = np.loadtxt(DTM_dir+file_2, delimiter=',')
f2_bool = f2[:, 2] != -9999
f2 = f2[f2_bool]
pdok_xyz = []
for i in f2:
    try:
        pdok_xyz.append([i[0], i[1], dt.interpolate_laplace(i[0], i[1])])
    except:
        pdok_xyz.append([i[0], i[1], -9999])
pdok_xyz = np.array(pdok_xyz)
pdok_xyz_bool = pdok_xyz[:, 2] != -9999  # to seperate no data values
pdok_xyz_fil = pdok_xyz[pdok_xyz_bool]
f2_fil = f2[pdok_xyz_bool]  # to retain only the common pixels
print(f2_fil.shape)
print(pdok_xyz_fil.shape)

# # data comparison
RMSE = np.around(rmse(pdok_xyz_fil[:, 2], f2_fil[:, 2]), decimals=4)
NRMSE = np.around(nrmse(pdok_xyz_fil[:, 2], f2_fil[:, 2]), decimals=4)
Rsquared = np.around(r_squared(pdok_xyz_fil[:, 2], f2_fil[:, 2]), decimals=4)
MI = np.around(mutual_information(pdok_xyz_fil[:, 2], f2_fil[:, 2]), decimals=4)
#
print("RMSE:", RMSE)
print("NRMSE:", NRMSE)
print("R-squared:", Rsquared)
print("Mutual information:", MI)
