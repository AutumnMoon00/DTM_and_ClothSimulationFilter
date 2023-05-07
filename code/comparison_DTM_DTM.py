from user_inputs import DTM_dir, file_1, file_2
from functions import r_squared, rmse, nrmse, mutual_information
import numpy as np
import rasterio

# data loading

f1 = np.loadtxt(DTM_dir+file_1, delimiter=',')
f2 = np.loadtxt(DTM_dir+file_2, delimiter=',')

# indexes of data pixels
f1_bool = f1[:, 2] != -9999
f2_bool = f2[:, 2] != -9999
true_data_idxs = np.logical_and(f1_bool, f2_bool)  # boolean array where data is available

f1_fil = f1[true_data_idxs]
f2_fil = f2[true_data_idxs]

# data comparison
RMSE = np.around(rmse(f1_fil[:, 2], f2_fil[:, 2]), decimals=4)
NRMSE = np.around(nrmse(f1_fil[:, 2], f2_fil[:, 2]), decimals=4)
Rsquared = np.around(r_squared(f1_fil[:, 2], f2_fil[:, 2]), decimals=4)
MI = np.around(mutual_information(f1_fil[:, 2], f2_fil[:, 2]), decimals=4)

print("RMSE:", RMSE)
print("NRMSE:", NRMSE)
print("R-squared:", Rsquared)
print("Mutual information:", MI)
