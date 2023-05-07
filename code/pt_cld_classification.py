from user_inputs import cloth_out_dir, ic_cloth_file, output_dir, pt_cld_to_classify, e_tol, class_pt_dir
import numpy as np
import laspy
from scipy.spatial import KDTree

# loading cloth data (cloth is txt file always, output from CSF.py)
cloth_data = np.loadtxt(cloth_out_dir + ic_cloth_file, delimiter=',')
# building a KD Tree of the point cloud
kd = KDTree(cloth_data[:, :2])
# print(cloth_data)

with laspy.open(output_dir + pt_cld_to_classify) as f:
    pt_cloud = f.read()
    xyz = pt_cloud.xyz.copy()
    pt_z = xyz[:, 2]

    # querying the closest point in cloth for every point in cloud
    dd, ii = kd.query(xyz[:, :2])
    corresponding_z = cloth_data[ii][:, 2]

    gap = abs(pt_z - corresponding_z)
    ground_pt_label = gap < e_tol
    class_copy = np.array(pt_cloud.classification.copy())

    classification = np.array([0] * class_copy.shape[0])
    classification[ground_pt_label] = 2

    # # output of classified points in laz
    out_classified_pts_laz = laspy.LasData(pt_cloud.header)
    out_classified_pts_laz.points = pt_cloud.points.copy()
    out_classified_pts_laz.classification = classification
    out_classified_pts_laz.write(class_pt_dir + pt_cld_to_classify[:-4] + "_reclassified" + ".laz")

    # # output of classified points in txt
    xy_class = np.vstack((xyz[:, 0], xyz[:, 1], classification)).transpose()
    np.savetxt(class_pt_dir + pt_cld_to_classify[:-4] + "_reclassified" + ".txt", xy_class, delimiter=',')
