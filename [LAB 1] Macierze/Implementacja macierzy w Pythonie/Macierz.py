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


def transpose_matrix(mat: Matrix) -> Matrix:
    new_mat = [[mat[j][i] for j in range(mat.size()[0])] for i in range(mat.size()[1])]
    return Matrix(new_mat)


def main():
    m = Matrix([[1, 0, 2],
                [-1, 3, 1]])

    print(transpose_matrix(m))

    m_ones = Matrix(arg=(2, 3), par=1)

    print(m + m_ones)

    m_for_mul = Matrix([[3, 1],
                        [2, 1],
                        [1, 0]])

    print(m * m_for_mul)


if __name__ == "__main__":
    main()
