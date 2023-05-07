import numpy as np
from sklearn.metrics import mutual_info_score


def divide_box(lower_left, upper_right, box_size):
    x1, y1 = lower_left
    x2, y2 = upper_right
    small_boxes = []
    for i in range(x1, x2, box_size):
        for j in range(y1, y2, box_size):
            small_boxes.append(((i, j), (i + box_size, j + box_size)))
    return small_boxes


def adjacent_vertices_values(grid):
    rows, cols = grid.shape
    adj_vertices = []
    for row in range(rows):
        for col in range(cols):
            if row < rows - 1:
                adj_vertices.append((grid[row][col], grid[row + 1][col]))
            if col < cols - 1:
                adj_vertices.append((grid[row][col], grid[row][col + 1]))
    return adj_vertices


def rmse(a, b):
    return np.sqrt(np.mean((a - b) ** 2))


def nrmse(a, b):
    return np.sqrt(np.mean((a - b) ** 2)) / (np.max(a) - np.min(a))


def r_squared(a, b):
    a_mean = np.mean(a)
    b_mean = np.mean(b)
    ss_tot = np.sum((a - a_mean) ** 2)
    ss_res = np.sum((a - b) ** 2)
    r_squared = 1 - (ss_res / ss_tot)
    return r_squared


def mutual_information(a, b):
    return mutual_info_score(a, b)


