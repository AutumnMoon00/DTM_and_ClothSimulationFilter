import numpy as np
import matplotlib
from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter, PillowWriter
import laspy
from scipy.spatial import KDTree
from user_inputs import cloth_resolution, tension, output_dir, output_file, in_file_CSF, cloth_out_dir
from user_inputs import left, bottom, right, top
from functions import adjacent_vertices_values

ezmax = 0.02  # threshold to stop looping
baby_steps = 0.1  # fall due to gravity = 10 cm

plt.rcParams['animation.ffmpeg_path'] = 'C:\\Users\\Sharath Chandra\\Downloads\\ffmpeg-2023-01-22-git-9d5e66942c-essentials_build\\bin\\ffmpeg.exe'
metadata = dict(title='ClothFalling', artist='AutumnMoon')
writer = FFMpegWriter(fps=15, metadata=metadata)

fig, ax = plt.subplots(subplot_kw=dict(projection='3d'), figsize=(10, 10))

plt.xlim(left-50, right+50)
plt.ylim(bottom-50, top+50)


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
z0 = max_ele + (10 * baby_steps)
decimals = 5
Pzmin = xyz_invert[kd.query(cloth_coordinates, k=1)[1]][:, 2]
Pzcur = np.linspace(z0, z0, cloth_coordinates.shape[0])
Pzprev = Pzcur + baby_steps
move = np.array([True] * cloth_coordinates.shape[0])  # cloth point can move if it's true

delta_z = abs(Pzcur - Pzprev).max()
count = 0

with writer.saving(fig, "CSF_tension_0.25.mp4", 200):
    while delta_z >= ezmax:
        # print(tension)
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

        pz_grid = Pzcur.reshape(xc.shape[0], yc.shape[0])
        ax.set_zlim(-53, -13)
        ax.set_title("CSF tension=0.25")
        ax.plot_surface(xc_co, yc_co, pz_grid+0.5, cmap=cm.viridis)
        ax.scatter(xyz_invert[::50, 0], xyz_invert[::50, 1], xyz_invert[::50, 2], c=xyz_invert[::50, 2], s=0.05, cmap='rainbow')
        # plt.show()
        writer.grab_frame()
        plt.cla()

        print(count, delta_z, Pzcur.min(), np.sum(move), cloth_coordinates.shape[0])
        count += 1
