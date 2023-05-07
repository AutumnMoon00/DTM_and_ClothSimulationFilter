# # user inputs section start here
file_path = "D:\\Geomatics\\Geo1015 DTM\\asgns\\4\\data\\C_52GN2.LAZ"  # path to laz file downloaded from PDOK
output_dir = "D:\\Geomatics\\Geo1015 DTM\\asgns\\4\\py_files\\code_v3\\extracted_and_thinning_points\\"  # directory
            # to store extracted points and thinning points
output_file = file_path.split('\\')[-1][:-4] + "_clip"   # do not give the extension. Extension will be given automatically
left, bottom = 208500, 385500
right, top = 209000, 386000
clipping = True

# Thinning
# if True choose from the following
# available methods nth_point, random_percentage, grid
thinning_boolean = True
thinning_methods = ["nth_point", "random_percentage", "grid"]  # "nth_point", "random_percentage", "grid"
n_value = 2  # for nth_point thinning
percentage = 10  # for random percentage thinning
grid_resolution = 5


# # inputs for cloth simulation
cloth_out_dir = "D:\\Geomatics\\Geo1015 DTM\\asgns\\4\\py_files\\code_v3\\cloth_folder\\"
in_file_CSF = "C_52GN2_clip_10percentage.laz"
cloth_resolution = 2
tension = 0.0

# # inputs for points classification
class_pt_dir = "D:\\Geomatics\\Geo1015 DTM\\asgns\\4\\py_files\\code_v3\\classified_point_clouds\\"
ic_cloth_file = "C_52GN2_clip_2th_point_cloth_ten0.5_res5.txt"  # input classification cloth file
pt_cld_to_classify = "C_52GN2_clip_2th_point.laz"
e_tol = 0.05  # 5 cm --> tolerance limit to classify points in points cloud as ground if they are within this threshold


# # inputs for laplace
classified_ptcld_dir = "D:\\Geomatics\\Geo1015 DTM\\asgns\\4\\py_files\\code_v3\\classified_point_clouds\\"
in_file_ptcld_for_laplace = "C_52GN2_clip_reclassified.laz"
DTM_dir = "D:\\Geomatics\\Geo1015 DTM\\asgns\\4\\py_files\\code_v3\\resampled_dtm\\"

# # inputs for natural neighbour
in_cloth_file_for_nni = "C_52GN2_clip_cloth_ten0.5_res5.txt"  # cloth file to be
grid_resolution = 0.5


# # user inputs for dtm comparisons
file_1 = "M_52GN2_50cm_clipped.tif"
file_2 = "C_52GN2_clip_10percentage_reclassified_resampled_laplace_grid.txt"


# # user inputs for isolines generation
fname_iso = "C:\\Users\\vidus\\Desktop\\DTM_Ass5_PointCloud\\SharathVBFiles\\forIsolines_C_52GN2_clip_10percentage_reclassified_resampled_laplace_grid.txt"
ci = 2  # this is contour step
contour_start = 15  # starting contour line
contour_end = 25  # end contour line
