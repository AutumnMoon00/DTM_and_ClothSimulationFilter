import laspy
import numpy as np
from user_inputs import file_path, output_dir, output_file, left, right, bottom, top, thinning_boolean
from user_inputs import clipping, thinning_methods, n_value, percentage, grid_resolution
from functions import divide_box

points_per_iter = 1000000
x_size = 500
y_size = 500

if clipping:

    with laspy.open(file_path) as f:
        outfile_laz = laspy.open(output_dir + output_file + ".laz", mode="w", header=f.header)
        total_point_count = f.header.point_count
        count = 0
        for points in f.chunk_iterator(points_per_iter):
            # For performance, we need to use copy
            # so that the underlying arrays are contiguous
            x, y = points.x.copy(), points.y.copy()
            point_piped = 0
            mask = (x >= left) & (x <= right) & (y >= bottom) & (y <= top)
            sub_points = points[mask].copy()
            outfile_laz.write_points(sub_points)
            count += len(points)
            print(f"points checked %: {np.around(count / total_point_count * 100, decimals=2)}")
            print(f"points appended: {outfile_laz.header.point_count}")

        outfile_laz.close()

    # writing the clipped points to txt file
    with laspy.open(output_dir+output_file+".laz") as f2:
        pts = f2.read()
        pts_classification = pts.classification
        pts = np.vstack((pts.x, pts.y, pts.z, pts.classification))
        pts = pts.transpose()
        np.savetxt(output_dir+output_file+".txt", pts, delimiter=',')


if thinning_boolean:

    with laspy.open(output_dir + output_file + ".laz") as f3:
        pts = f3.read()

        for method in thinning_methods:
            if method == "nth_point":
                n = n_value
                mask = [False] * len(pts)
                mask = np.array(mask)
                true_idxs = np.arange(n, len(pts), n)
                mask[true_idxs] = np.array([True] * true_idxs.shape[0])

                outfile_npt_laz = laspy.LasData(pts.header)
                pts_copy_nth = pts.points[mask].copy()
                outfile_npt_laz.points = pts_copy_nth
                outfile_npt_laz.write(output_dir+output_file+f"_{n}th_point"+".laz")

                pts_nth = np.vstack((pts.points[mask].x, pts.points[mask].y, pts.points[mask].z,
                                     pts.points[mask].classification))
                np.savetxt(output_dir + output_file + f"_{n}th_point" +".txt", pts_nth.transpose(), delimiter=',')
                print("nth_point_done")

            if method == "random_percentage":
                num = int(len(pts) * percentage / 100)
                indices = np.random.choice(len(pts), num, replace=False)  # indexes of the pts to be chosen
                mask = np.array([False] * len(pts))
                mask[indices] = np.array([True] * indices.shape[0])
                outfile_percent_laz = laspy.LasData(pts.header)
                pts_copy_random = pts.points[mask].copy()
                outfile_percent_laz.points = pts_copy_random
                outfile_percent_laz.write(output_dir + output_file + f"_{percentage}percentage" + ".laz")

                pts_nth = np.vstack((pts.points[mask].x, pts.points[mask].y, pts.points[mask].z,
                                     pts.points[mask].classification))
                np.savetxt(output_dir + output_file + f"_{percentage}percentage" +".txt",
                           pts_nth.transpose(), delimiter=',')
                print("random_percentage_done")

            if method == "grid":
                xyz = pts.xyz.copy()
                x = xyz[:, 0]
                y = xyz[:, 1]
                z = xyz[:, 2]
                holder = []
                boxes = divide_box((left, bottom), (right, top), grid_resolution)
                for box in boxes:
                    mask1 = x >= box[0][0]
                    mask2 = x <= box[1][0]
                    mask3 = y >= box[0][1]
                    mask4 = y <= box[1][1]
                    mask = mask1 & mask2 & mask3 & mask4
                    pts_in_box = xyz[mask]

                    if pts_in_box.shape[0] != 0:
                        box_pt = np.array([(box[0][0] + box[1][0]) / 2, (box[0][1] + box[1][1]) / 2,
                                           np.mean(pts_in_box[:, 2])])
                    else:
                        box_pt = np.array([(box[0][0] + box[1][0]) / 2, (box[0][1] + box[1][1]) / 2, np.nan])

                    holder.append(box_pt)
                np.savetxt(output_dir+output_file+f"_{grid_resolution}m_grid.txt", np.vstack(holder), delimiter=',')

                print("grid_done")

