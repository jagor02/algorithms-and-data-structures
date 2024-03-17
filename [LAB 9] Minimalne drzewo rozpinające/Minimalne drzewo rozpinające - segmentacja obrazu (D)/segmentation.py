# skończone
import cv2
import numpy as np


class Vertex:
    def __init__(self, key, color=None):
        self.key = key
        self.color = color

    def __eq__(self, other_vertex):
        return self.key == other_vertex.key

    def __hash__(self):
        return hash(self.key)

    def get_color(self):
        return self.color

    def set_color(self, color):
        self.color = color


class Edge:
    pass


class AdjList:
    def __init__(self):
        self.list = {}
        self.vertex_dict = {}

    def isEmpty(self):
        return True if self.list == {} else False

    def insertVertex(self, vertex):
        self.list[vertex] = {}
        self.vertex_dict[vertex] = self.order()

    def insertEdge(self, vertex1, vertex2, edge=None):
        (self.list[vertex1])[vertex2] = edge

    def deleteVertex(self, vertex):
        for vert in self.neighbours(self.getVertexIdx(vertex)):
            del self.list[vert][vertex]
        del self.list[vertex]
        del self.vertex_dict[vertex]

    def deleteEdge(self, vertex1, vertex2):
        del (self.list[vertex1])[vertex2]

    def getVertexIdx(self, vertex):
        return self.vertex_dict[vertex]

    def getVertex(self, vertex_idx):
        for vert, idx in self.vertex_dict.items():
            if vertex_idx == idx:
                return vert
        return None

    def neighboursIdx(self, vertex_idx):
        return [self.getVertexIdx(vert) for vert in (self.list[self.getVertex(vertex_idx)]).keys()]

    def neighbours(self, vertex_idx):
        return self.list[self.getVertex(vertex_idx)]

    def order(self):
        return len(self.vertex_dict)

    def size(self):
        if not self.isEmpty():
            s = 0
            for vert in self.list:
                for _ in self.list[vert]:
                    s += 1
            return s
        else:
            return 0

    def edges(self):
        edge_table = []
        for vert in self.list.keys():
            for v in (self.list[vert]).keys():
                edge_table.append((vert.key, v.key, self.list[vert][v]))
        return edge_table


def Prim(graph, start_vertex_idx):
    intree = [0 for _ in range(graph.order())]
    distance = [float('inf') for _ in range(graph.order())]
    parent = [-1 for _ in range(graph.order())]

    graph_tree = AdjList()
    for idx in range(graph.order()):
        graph_tree.insertVertex(graph.getVertex(idx))

    v = start_vertex_idx

    weight_sum = 0

    while intree[v] == 0:
        intree[v] = 1

        for neigh, weight in graph.neighbours(v).items():
            if distance[graph.getVertexIdx(neigh)] > weight and intree[graph.getVertexIdx(neigh)] == 0:
                distance[graph.getVertexIdx(neigh)] = weight
                parent[graph.getVertexIdx(neigh)] = v

        min_value = float('inf')

        for i in range(graph.order()):
            if intree[i] == 0:
                if min_value > distance[i]:
                    v = i
                    min_value = distance[i]

        if intree[v] == 0:
            graph_tree.insertEdge(graph.getVertex(parent[v]), graph.getVertex(v), min_value)
            graph_tree.insertEdge(graph.getVertex(v), graph.getVertex(parent[v]), min_value)

        weight_sum += min_value

    return graph_tree, weight_sum


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


def BFS(graph, start_vertex, color):
    start_vertex.set_color(color)
    visited = [start_vertex]
    queue = [start_vertex]
    while not queue == []:
        vertex = queue.pop(0)
        for vert in graph.neighbours(graph.getVertexIdx(vertex)):
            if vert not in visited and vert not in queue:
                vert.set_color(color)
                visited.append(vert)
                queue.append(vert)
    return visited


def segmentation(image):
    graph = AdjList()
    I = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
    (Y, X) = I.shape
    for y in range(Y):
        for x in range(X):
            graph.insertVertex(Vertex(X * y + x))
    for y in range(Y):
        for x in range(X):
            if y == 0 and x == 0:
                for j in range(0, 2):
                    for i in range(0, 2):
                        if not (j == 0 and i == 0):
                            graph.insertEdge(Vertex(X * 0 + 0), Vertex(X * j + i), abs(I[0, 0] - I[j, i]))
            elif y == Y - 1 and x == 0:
                for j in range(Y - 2, Y):
                    for i in range(0, 2):
                        if not (j == Y - 1 and i == 0):
                            graph.insertEdge(Vertex(X * (Y - 1) + 0), Vertex(X * j + i), abs(I[Y - 1, 0] - I[j, i]))
            elif y == 0 and x == X - 1:
                for j in range(0, 2):
                    for i in range(X - 2, X):
                        if not (j == 0 and i == X - 1):
                            graph.insertEdge(Vertex(X * 0 + (X - 1)), Vertex(X * j + i), abs(I[0, X - 1] - I[j, i]))
            elif y == Y - 1 and x == X - 1:
                for j in range(Y - 2, Y):
                    for i in range(X - 2, X):
                        if not (j == Y - 1 and i == X - 1):
                            graph.insertEdge(Vertex(X * (Y - 1) + (X - 1)), Vertex(X * j + i),
                                             abs(I[Y - 1, X - 1] - I[j, i]))
            elif y == 0:
                for j in range(0, 2):
                    for i in range(x - 1, x + 2):
                        if not (j == 0 and i == x):
                            graph.insertEdge(Vertex(X * 0 + x), Vertex(X * j + i), abs(I[0, x] - I[j, i]))
            elif y == Y - 1:
                for j in range(Y - 2, Y):
                    for i in range(x - 1, x + 2):
                        if not (j == Y - 1 and i == x):
                            graph.insertEdge(Vertex(X * (Y - 1) + x), Vertex(X * j + i), abs(I[Y - 1, x] - I[j, i]))
            elif x == 0:
                for j in range(y - 1, y + 2):
                    for i in range(0, 2):
                        if not (j == y and i == 0):
                            graph.insertEdge(Vertex(X * y + 0), Vertex(X * j + i), abs(I[y, 0] - I[j, i]))
            elif x == X - 1:
                for j in range(y - 1, y + 2):
                    for i in range(X - 2, X):
                        if not (j == y and i == X - 1):
                            graph.insertEdge(Vertex(X * y + (X - 1)), Vertex(X * j + i), abs(I[y, X - 1] - I[j, i]))
            else:
                for j in range(y - 1, y + 2):
                    for i in range(x - 1, x + 2):
                        if not (j == y and i == x):
                            graph.insertEdge(Vertex(X * y + x), Vertex(X * j + i), abs(I[y, x] - I[j, i]))
    graph_Prim = Prim(graph, 0)[0]
    edges = graph_Prim.edges()
    max_edge = edges[0]
    for edge in edges:
        if max_edge[2] < edge[2]:
            max_edge = edge
    v1 = graph.getVertex(max_edge[0])
    v2 = graph.getVertex(max_edge[1])
    graph_Prim.deleteEdge(v1, v2)
    graph_Prim.deleteEdge(v2, v1)
    IS = np.zeros((Y, X), dtype='uint8')
    visited_100 = BFS(graph_Prim, v1, 100)
    visited_200 = BFS(graph_Prim, v2, 200)
    for vert in visited_100:
        y = vert.key // X
        x = vert.key % X
        IS[y, x] = vert.get_color()
    for vert in visited_200:
        y = vert.key // X
        x = vert.key % X
        IS[y, x] = vert.get_color()
    cv2.imshow("Wynik", IS)
    cv2.waitKey()


def main():
    image = "sample.png"
    segmentation(image)


if __name__ == "__main__":
    main()
