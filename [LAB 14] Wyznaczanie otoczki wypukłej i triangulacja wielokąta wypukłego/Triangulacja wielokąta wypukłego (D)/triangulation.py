# skończone
import time
import numpy as np


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y


def triangulation(list_of_points, i, j):
    min_cost = None
    if j - i + 1 >= 3:
        for k in range(i + 1, j):
            # triangle = (i, k, j)
            min_cost_figure_left = triangulation(list_of_points, i, k)
            min_cost_figure_right = triangulation(list_of_points, k, j)
            p1 = list_of_points[i]
            p2 = list_of_points[k]
            p3 = list_of_points[j]
            min_cost_triangle = np.sqrt((p1.get_x() - p2.get_x()) ** 2 + (p1.get_y() - p2.get_y()) ** 2) + \
                                np.sqrt((p1.get_x() - p3.get_x()) ** 2 + (p1.get_y() - p3.get_y()) ** 2) + \
                                np.sqrt((p3.get_x() - p2.get_x()) ** 2 + (p3.get_y() - p2.get_y()) ** 2)
            sub_min_cost = min_cost_triangle
            if min_cost_figure_left is not None:
                sub_min_cost += min_cost_figure_left
            if min_cost_figure_right is not None:
                sub_min_cost += min_cost_figure_right
            if min_cost is None or min_cost > sub_min_cost:
                min_cost = sub_min_cost
    return min_cost


def triangulation_PD(list_of_points):
    len_points = len(list_of_points)
    if len_points >= 3:
        D = [[None for _ in range(len_points)] for _ in range(len_points)]
        for i in range(len_points):
            k = (i + 1) % len_points
            j = (i + 2) % len_points
            p1 = list_of_points[i]
            p2 = list_of_points[k]
            p3 = list_of_points[j]
            D[i][j] = np.sqrt((p1.get_x() - p2.get_x()) ** 2 + (p1.get_y() - p2.get_y()) ** 2) + \
                      np.sqrt((p1.get_x() - p3.get_x()) ** 2 + (p1.get_y() - p3.get_y()) ** 2) + \
                      np.sqrt((p3.get_x() - p2.get_x()) ** 2 + (p3.get_y() - p2.get_y()) ** 2)
        for lenn in range(3, len_points):
            i = 0
            for j in range(lenn+i, len_points):
                p1 = list_of_points[i]
                p3 = list_of_points[j]
                min_cost = float('inf')
                for k in range(i+1, j):
                    p2 = list_of_points[k]
                    triangle = np.sqrt((p1.get_x() - p2.get_x()) ** 2 + (p1.get_y() - p2.get_y()) ** 2) + \
                               np.sqrt((p1.get_x() - p3.get_x()) ** 2 + (p1.get_y() - p3.get_y()) ** 2) + \
                               np.sqrt((p3.get_x() - p2.get_x()) ** 2 + (p3.get_y() - p2.get_y()) ** 2)
                    if D[i][k] is None:
                        left_fig = 0
                    else:
                        left_fig = D[i][k]
                    if D[k][j] is None:
                        right_fig = 0
                    else:
                        right_fig = D[k][j]
                    possible_new_min_cost = left_fig + right_fig + triangle
                    if min_cost > possible_new_min_cost:
                        min_cost = possible_new_min_cost
                D[i][j] = min_cost
                i += 1
        return D[0][len_points-1]
    return 0


def main():
    list_of_points1 = []
    list_of_coords1 = [[0, 0], [1, 0], [2, 1], [1, 2], [0, 2]]
    for coords in list_of_coords1:
        list_of_points1.append(Point(coords[0], coords[1]))

    t_start = time.perf_counter()
    min_cost = triangulation(list_of_points1, 0, len(list_of_points1) - 1)
    t_stop = time.perf_counter()
    print("Czas obliczeń:", "{:.7f}".format(t_stop - t_start))

    print(min_cost)

    list_of_points2 = []
    list_of_coords2 = [[0, 0], [4, 0], [5, 4], [4, 5], [2, 5], [1, 4], [0, 3], [0, 2]]
    for coords in list_of_coords2:
        list_of_points2.append(Point(coords[0], coords[1]))

    t_start = time.perf_counter()
    min_cost = triangulation(list_of_points2, 0, len(list_of_points2) - 1)
    t_stop = time.perf_counter()
    print("Czas obliczeń:", "{:.7f}".format(t_stop - t_start))

    print(min_cost)

    t_start = time.perf_counter()
    min_cost = triangulation_PD(list_of_points1)
    t_stop = time.perf_counter()
    print("Czas obliczeń:", "{:.7f}".format(t_stop - t_start))

    print(min_cost)

    t_start = time.perf_counter()
    min_cost = triangulation_PD(list_of_points2)
    t_stop = time.perf_counter()
    print("Czas obliczeń:", "{:.7f}".format(t_stop - t_start))

    print(min_cost)


if __name__ == "__main__":
    main()
