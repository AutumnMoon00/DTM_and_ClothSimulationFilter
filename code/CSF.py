import laspy
import numpy as np
from scipy.spatial import KDTree
from user_inputs import cloth_resolution, tension, output_dir, output_file, in_file_CSF, cloth_out_dir
from user_inputs import left, bottom, right, top
from functions import adjacent_vertices_values

ezmax = 0.01  # threshold to stop looping
baby_steps = 0.1  # fall due to gravity = 10 cm

if in_file_CSF[-3:] == "laz":
    print("yes")
    with laspy.open(output_dir + in_file_CSF) as f:
        pt_cloud = f.read()
        xyz = pt_cloud.xyz.copy()  # reading the clipped points
        xyz_invert = xyz.copy()  # making a copy of only x, y, z values of the clipped points
        xyz_invert[:, 2] = -xyz_invert[:, 2]  # inverting it
        if "grid" not in in_file_CSF:
            clas = np.array(list(pt_cloud.classification.copy()))

if in_file_CSF[-3:] == "txt":
    pt_cloud = np.loadtxt(output_dir + in_file_CSF, delimiter=',')
    x = pt_cloud[:, 0]
    y = pt_cloud[:, 1]
    z = pt_cloud[:, 2]
    xyz = np.vstack((x, y, z)).transpose()
    if "grid" not in in_file_CSF:
        clas = pt_cloud[:, 3].astype(int)
    xyz_invert = xyz
    xyz_invert[:, 2] = -xyz_invert[:, 2]

# building a KD Tree of the point cloud
kd = KDTree(xyz[:, :2])

# cloth grid points
xc = np.arange(left, right, cloth_resolution)
yc = np.arange(bottom, top, cloth_resolution)
xc_co, yc_co = np.meshgrid(xc, yc)
cloth_coordinates = np.c_[np.ravel(xc_co), np.ravel(yc_co)]

# indexes for the points
pt_indexes = np.arange(0, xc.shape[0] * yc.shape[0], 1).reshape((xc.shape[0], yc.shape[0]))
edges = adjacent_vertices_values(pt_indexes)
edges = np.array(edges)

# max elevation in inverted pt cloud
max_ele = xyz_invert[:, 2].max()

# initializing cloth at (3*baby_steps) m above max elevation of z_invert
z0 = max_ele + (3 * baby_steps)
decimals = 5
Pzmin = xyz_invert[kd.query(cloth_coordinates, k=1)[1]][:, 2]
Pzcur = np.linspace(z0, z0, cloth_coordinates.shape[0])
Pzprev = Pzcur + baby_steps
move = np.array([True] * cloth_coordinates.shape[0])  # cloth point can move if it's true

delta_z = abs(Pzcur - Pzprev).max()
count = 0

while delta_z >= ezmax:
    # Gravity Falls
    # indexes of True in move
    true_idx = np.nonzero(move == True)
    tmp = Pzcur[true_idx]
    Pzcur[true_idx] -= baby_steps  # with every iteration movable points going down by baby_step
    Pzprev[true_idx] = tmp

    # internal forces
    for e in edges:
        p0 = e[0]  # estart index
        p1 = e[1]  # eend index
        z_p0 = Pzcur[p0]
        z_p1 = Pzcur[p1]

        if move[p0] and move[p1]:
            Pzcur[p0] = z_p0 + (z_p1 - z_p0) * tension / 2
            Pzcur[p1] = z_p1 + (z_p0 - z_p1) * tension / 2

        elif move[p0] and (move[p1] is not True):
            Pzcur[p0] = z_p0 + (z_p1 - z_p0) * tension

        elif move[p1] and (move[p0] is not True):
            Pzcur[p1] = z_p1 + (z_p0 - z_p1) * tension

        # updating move-ability (aka mobility)
        below_true_idx = np.nonzero(Pzcur < Pzmin)
        tmp2 = Pzmin[below_true_idx]
        Pzcur[below_true_idx] = tmp2
        Pzprev[below_true_idx] = tmp2
        move = Pzcur > Pzmin
        move_idx = np.nonzero(move == True)
        if move_idx[0].shape[0] > 0:
            delta_z = abs(Pzcur[move_idx] - Pzprev[move_idx]).max()
        else:
            delta_z = 0

    print(count, delta_z, Pzcur.min(), np.sum(move), cloth_coordinates.shape[0])
    count += 1

z_corrected = -Pzcur
cloth_coordinates_actual = np.vstack((cloth_coordinates[:, 0], cloth_coordinates[:, 1], z_corrected)).transpose()
np.savetxt(cloth_out_dir+in_file_CSF[:-4]+f"_cloth_ten{tension}_res{cloth_resolution}.txt", cloth_coordinates_actual, delimiter=',')
