# skończone
from typing import Tuple


class Matrix:
    def __init__(self, arg, par=0):
        if isinstance(arg, Tuple):
            if len(arg) == 2:
                if arg[0] > 0 and arg[1] > 0:
                    self.__matrix = [[par] * arg[1] for _ in range(arg[0])]
                else:
                    raise Exception("Matrix must have positive size values.")
            else:
                raise Exception("Matrix must be 2-dimensional.")
        else:
            self.__matrix = arg

    def __add__(self, mat):
        if self.size() == mat.size():
            new_mat = [[self.__matrix[i][j] + mat[i][j] for j in range(self.size()[1])] for i in range(self.size()[0])]
            return Matrix(new_mat)
        else:
            raise Exception("Given matrixes have different shapes.")

    def __mul__(self, mat):
        if self.size()[0] == mat.size()[1] and self.size()[1] == mat.size()[0]:
            new_mat = Matrix(arg=(self.size()[0], self.size()[0]), par=0)
            for i in range(self.size()[0]):
                for j in range(mat.size()[1]):
                    for k in range(self.size()[1]):
                        new_mat[i][j] += self.__matrix[i][k] * mat[k][j]
            return new_mat
        else:
            raise Exception("Given matrixes cannot be multiplied.")

    def __getitem__(self, num):
        return self.__matrix[num]

    def __str__(self):
        str_matrix = ''
        for i in range(self.size()[0]):
            str_matrix += '|'
            for j in range(self.size()[1]):
                str_matrix += ' ' + str(self.__matrix[i][j])
            str_matrix += ' |\n'
        return str_matrix

    def size(self):
        return len(self.__matrix), len(self.__matrix[0])


def determinant_for_2x2_matrix(mat: Matrix, i: int, j: int, k: int = 0, m: int = 0) -> float:
    return mat[k][m] * mat[i][j] - mat[i][m] * mat[k][j]


def chio(mat: Matrix) -> float:
    if mat.size()[0] == mat.size()[1]:
        if mat.size()[0] > 2:
            k = 0
            m = 0
            while mat[k][m] == 0 and mat[m][k] == 0 and k < mat.size()[0]:
                m = 0
                k += 1
                while mat[k][m] == 0 and mat[m][k] == 0 and m <= k:
                    m += 1
            if mat[m][k] != 0 and m != k:
                k, m = m, k
            if mat[k][m] != 0:
                new_mat = [[determinant_for_2x2_matrix(mat, i, j, k, m) for j in range(mat.size()[1]) if j != m] for i
                           in range(mat.size()[0]) if i != k]
                det = (1 / mat[k][m] ** (mat.size()[0] - 2)) * chio(Matrix(new_mat))
                if (k == 0 and m == 0) or (k != 0 and m != 0):
                    return det
                else:
                    return -det
            else:
                raise Exception("Chio method cannot be used.")
        elif mat.size()[0] == 2:
            return determinant_for_2x2_matrix(mat, 1, 1)
        elif mat.size()[0] == 1:
            return mat[0][0]
    else:
        raise Exception("It isn't a square matrix.")


def main():
    m1 = Matrix([[5, 1, 1, 2, 3],
                 [4, 2, 1, 7, 3],
                 [2, 1, 2, 4, 7],
                 [9, 1, 0, 7, 0],
                 [1, 4, 7, 2, 2]])

    print(chio(m1))

    m2 = Matrix([[0, 1, 1, 2, 3],
                 [4, 2, 1, 7, 3],
                 [2, 1, 2, 4, 7],
                 [9, 1, 0, 7, 0],
                 [1, 4, 7, 2, 2]])

    print(chio(m2))


if __name__ == "__main__":
    main()
