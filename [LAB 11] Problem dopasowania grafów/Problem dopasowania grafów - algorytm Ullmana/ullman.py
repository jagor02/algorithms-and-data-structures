# nieskończone
import numpy as np


class Vertex:
    def __init__(self, key):
        self.key = key

    def __eq__(self, other_vertex):
        return self.key == other_vertex.key

    def __hash__(self):
        return hash(self.key)

    def __repr__(self):
        return f"{self.key}"


class Edge:
    pass


class AdjMatrix:
    def __init__(self, mat_init_val=0):
        self.matrix = []
        self.vertex_dict = {}
        self.mat_init_val = mat_init_val

    def isEmpty(self):
        return True if self.matrix == [] else False

    def insertVertex(self, vertex):
        self.vertex_dict[vertex] = self.order()
        if not self.isEmpty():
            for lst in self.matrix:
                lst.append(self.mat_init_val)
        self.matrix.append([self.mat_init_val for _ in range(self.order())])

    def insertEdge(self, vertex1, vertex2, edge):
        id1 = self.getVertexIdx(vertex1)
        id2 = self.getVertexIdx(vertex2)
        self.matrix[id1][id2] = edge

    def deleteVertex(self, vertex):
        idx = self.getVertexIdx(vertex)
        del self.matrix[idx]
        for lst in self.matrix:
            del lst[idx]
        for i in range(idx + 1, self.order()):
            self.vertex_dict[self.getVertex(i)] -= 1
        del self.vertex_dict[vertex]

    def deleteEdge(self, vertex1, vertex2):
        id1 = self.getVertexIdx(vertex1)
        id2 = self.getVertexIdx(vertex2)
        self.matrix[id1][id2] = self.mat_init_val

    def getVertexIdx(self, vertex):
        return self.vertex_dict[vertex]

    def getVertex(self, vertex_idx):
        for vert, idx in self.vertex_dict.items():
            if vertex_idx == idx:
                return vert
        return None

    def neighboursIdx(self, vertex_idx):
        idx_table = []
        vert_table = self.neighbours(vertex_idx)
        for vert in vert_table:
            idx_table.append(self.getVertexIdx(vert))
        return idx_table

    def neighbours(self, vertex_idx):
        vert_table = {}
        idx = 0
        for edge in self.matrix[vertex_idx]:
            if edge != self.mat_init_val:
                vert_table[self.getVertex(idx)] = edge
            idx += 1
        return vert_table

    def order(self):
        return len(self.vertex_dict)

    def size(self):
        if not self.isEmpty():
            s = 0
            v_num = self.order()
            for i in range(v_num):
                for j in range(v_num):
                    if self.matrix[i][j] != self.mat_init_val:
                        s += 1
            return s
        else:
            return 0

    def edges(self):
        edge_table = []
        for i in range(self.order()):
            for j in range(self.order()):
                if self.matrix[i][j] != self.mat_init_val:
                    edge_table.append((self.getVertex(i).key, self.getVertex(j).key))
        return edge_table

    def getAdjMatrix(self):
        return self.matrix


def printGraph(g):
    n = g.order()
    print("------GRAPH------", n)
    for i in range(n):
        v = g.getVertex(i)
        print(v, end=" -> ")
        nbrs = g.neighbours(i)
        for (j, w) in nbrs.items():
            print(j, w, end=";")
        print()
    print("-------------------")


def Ullman_algorithm(graph_G, graph_P):
    g_G = AdjMatrix()
    existing_vertexes = []
    for ele in graph_G:
        if ele[0] not in existing_vertexes:
            g_G.insertVertex(Vertex(ele[0]))
            existing_vertexes.append(ele[0])
        if ele[1] not in existing_vertexes:
            g_G.insertVertex(Vertex(ele[1]))
            existing_vertexes.append(ele[1])
        g_G.insertEdge(Vertex(ele[0]), Vertex(ele[1]), ele[2])
        g_G.insertEdge(Vertex(ele[1]), Vertex(ele[0]), ele[2])
    # printGraph(g_G)

    g_P = AdjMatrix()
    existing_vertexes = []
    for ele in graph_P:
        if ele[0] not in existing_vertexes:
            g_P.insertVertex(Vertex(ele[0]))
            existing_vertexes.append(ele[0])
        if ele[1] not in existing_vertexes:
            g_P.insertVertex(Vertex(ele[1]))
            existing_vertexes.append(ele[1])
        g_P.insertEdge(Vertex(ele[0]), Vertex(ele[1]), ele[2])
        g_P.insertEdge(Vertex(ele[1]), Vertex(ele[0]), ele[2])
    # printGraph(g_P)

    matrix_G = g_G.getAdjMatrix()
    matrix_P = g_P.getAdjMatrix()

    matrix_G_np = np.array(matrix_G)
    matrix_P_np = np.array(matrix_P)

    M = np.zeros((g_P.order(), g_G.order()))

    M_variants_ullman_v1, no_recursion_ullman_v1 = Ullman_v1(0, M, matrix_G_np, matrix_P_np)

    M0 = np.zeros((g_P.order(), g_G.order()))

    for vi_idx in range(g_P.order()):
        edge_P_sum = 0
        for edge in matrix_P_np[:, vi_idx]:
            edge_P_sum += edge
        for edge in matrix_P_np[vi_idx, :]:
            edge_P_sum += edge
        for vj_idx in range(g_G.order()):
            edge_G_sum = 0
            for edge in matrix_G_np[:, vj_idx]:
                edge_G_sum += edge
            for edge in matrix_G_np[vj_idx, :]:
                edge_G_sum += edge
            if edge_P_sum <= edge_G_sum:
                M0[vi_idx, vj_idx] = 1

    M = np.zeros((g_P.order(), g_G.order()))

    M_variants_ullman_v2, no_recursion_ullman_v2 = Ullman_v2(0, M, matrix_G_np, matrix_P_np, M0)

    M = np.zeros((g_P.order(), g_G.order()))

    M_variants_ullman_v3, no_recursion_ullman_v3 = Ullman_v3(0, M0, matrix_G_np, matrix_P_np, g_G, g_P, M0)

    print(len(M_variants_ullman_v1), no_recursion_ullman_v1)
    print(len(M_variants_ullman_v2), no_recursion_ullman_v2)
    print(len(M_variants_ullman_v3), no_recursion_ullman_v3)


def Ullman_v1(actual_row, M, matrix_G, matrix_P, no_recursion=0, used_columns=None, M_variants=None):
    if used_columns is None:
        used_columns = [False for _ in range(M.shape[1])]
    if M_variants is None:
        M_variants = []
    if actual_row == M.shape[0]:
        if (matrix_P == np.dot(M, np.transpose(np.dot(M, matrix_G)))).all():
            M_variants.append(np.copy(M))
        return M_variants, no_recursion
    for c in range(M.shape[1]):
        if not used_columns[c]:
            used_columns[c] = True
            for c_repeat in range(M.shape[1]):
                M[actual_row, c_repeat] = 0
            M[actual_row, c] = 1
            no_recursion += 1
            M_variants, no_recursion = Ullman_v1(actual_row + 1, M, matrix_G, matrix_P, no_recursion, used_columns,
                                                 M_variants)
            used_columns[c] = False
    return M_variants, no_recursion


def Ullman_v2(actual_row, M, matrix_G, matrix_P, M0, no_recursion=0, used_columns=None, M_variants=None):
    if used_columns is None:
        used_columns = [False for _ in range(M.shape[1])]
    if M_variants is None:
        M_variants = []
    if actual_row == M.shape[0]:
        if (matrix_P == np.dot(M, np.transpose(np.dot(M, matrix_G)))).all():
            M_variants.append(np.copy(M))
        return M_variants, no_recursion
    for c in range(M.shape[1]):
        if not used_columns[c]:
            if M0[actual_row, c] == 1:
                used_columns[c] = True
                for c_repeat in range(M.shape[1]):
                    M[actual_row, c_repeat] = 0
                M[actual_row, c] = 1
                no_recursion += 1
                M_variants, no_recursion = Ullman_v2(actual_row + 1, M, matrix_G, matrix_P, M0, no_recursion,
                                                     used_columns, M_variants)
                used_columns[c] = False
    return M_variants, no_recursion


def Prune(M, M0, g_G, g_P):
    rep = True
    while rep:
        rep = False
        for i in range(M.shape[0]):
            for j in range(M.shape[1]):
                if M[i, j] == 1:
                    #print(g_P.neighboursIdx(i))
                    for x in g_P.neighboursIdx(i):
                        in_flag = True
                        for y in g_G.neighboursIdx(j):
                            if M[x, y] == 1:
                                in_flag = False
                                break
                        if in_flag:
                            M[i, j] = 0
                            rep = True
                            


def Ullman_v3(actual_row, M, matrix_G, matrix_P, g_G, g_P, M0, no_recursion=0, used_columns=None, M_variants=None):
    if used_columns is None:
        used_columns = [False for _ in range(M.shape[1])]
    if M_variants is None:
        M_variants = []
    if actual_row == M.shape[0]:
        if (matrix_P == np.dot(M, np.transpose(np.dot(M, matrix_G)))).all():
            M_variants.append(np.copy(M))
        return M_variants, no_recursion
    M_copy = np.copy(M)
    Prune(M_copy, M0, g_G, g_P)
    #print(M_copy)
    for c in range(M_copy.shape[1]):
        if not used_columns[c]:
            if M0[actual_row, c] == 1:
                used_columns[c] = True
                for c_repeat in range(M_copy.shape[1]):
                    M_copy[actual_row, c_repeat] = 0
                M_copy[actual_row, c] = 1
                no_recursion += 1
                M_variants, no_recursion = Ullman_v3(actual_row + 1, M_copy, matrix_G, matrix_P, g_G, g_P, M0,
                                                     no_recursion, used_columns, M_variants)
                used_columns[c] = False
    return M_variants, no_recursion


def main():
    graph_G = [('A', 'B', 1), ('B', 'F', 1), ('B', 'C', 1), ('C', 'D', 1), ('C', 'E', 1), ('D', 'E', 1)]
    graph_P = [('A', 'B', 1), ('B', 'C', 1), ('A', 'C', 1)]

    Ullman_algorithm(graph_G, graph_P)


if __name__ == "__main__":
    main()
