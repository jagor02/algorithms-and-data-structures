# skończone
import graf_mst


class Vertex:
    def __init__(self, key, color=None):
        self.key = key
        self.color = color

    def __eq__(self, other_vertex):
        return self.key == other_vertex.key

    def __hash__(self):
        return hash(self.key)

    def __repr__(self):
        return f"{self.key}"

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


class UnionFind:
    def __init__(self, n):
        self.p = [i for i in range(n)]
        self.size = [1 for _ in range(n)]
        self.n = n

    def find(self, v):
        if self.p[v] == v:
            return v
        else:
            return self.find(self.p[v])

    def union_sets(self, s1, s2):
        s1_root = self.find(s1)
        s2_root = self.find(s2)
        if s1_root != s2_root:
            s1_size = self.size[s1_root]
            s2_size = self.size[s2_root]
            if s1_size >= s2_size:
                self.p[s2_root] = s1_root
                self.size[s1_root] += 1
            else:
                self.p[s1_root] = s2_root
                self.size[s2_root] += 1

    def same_components(self, s1, s2):
        return self.find(s1) == self.find(s2)


def insertion_sort(table):
    for i in range(1, len(table)):
        buffor = table[i]
        flag = False
        for j in range(i - 1, -1, -1):
            if table[j][2] > buffor[2]:
                table[j + 1] = table[j]
            else:
                table[j + 1] = buffor
                flag = True
                break
        if not flag:
            table[0] = buffor


def toASCII(ele):
    return ord(ele)


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


def kruskal(graph):
    graph_kruskal = AdjList()

    for i in range(graph.order()):
        vert = graph.getVertex(i)
        graph_kruskal.insertVertex(vert)

    edges = graph.edges()
    insertion_sort(edges)

    union_find = UnionFind(graph_kruskal.order())

    for e in edges:
        if not union_find.same_components(graph_kruskal.getVertexIdx(Vertex(e[0])),
                                          graph_kruskal.getVertexIdx(Vertex(e[1]))):
            graph_kruskal.insertEdge(Vertex(e[0]), Vertex(e[1]), e[2])
            graph_kruskal.insertEdge(Vertex(e[1]), Vertex(e[0]), e[2])
            union_find.union_sets(graph_kruskal.getVertexIdx(Vertex(e[0])),
                                  graph_kruskal.getVertexIdx(Vertex(e[1])))

    return graph_kruskal


def main():
    union_find_test = UnionFind(5)

    union_find_test.union_sets(0, 1)
    union_find_test.union_sets(3, 4)

    print(union_find_test.same_components(0, 1))
    print(union_find_test.same_components(1, 2))
    print(union_find_test.same_components(3, 4))

    union_find_test.union_sets(2, 0)

    print(union_find_test.same_components(0, 1))
    print(union_find_test.same_components(1, 2))
    print(union_find_test.same_components(3, 4))

    graph = AdjList()

    existing_vertex = []

    for ele in graf_mst.graf:
        if ele[0] not in existing_vertex:
            graph.insertVertex(Vertex(ele[0]))
            existing_vertex.append(ele[0])
        if ele[1] not in existing_vertex:
            graph.insertVertex(Vertex(ele[1]))
            existing_vertex.append(ele[1])
        graph.insertEdge(Vertex(ele[0]), Vertex(ele[1]), ele[2])
        graph.insertEdge(Vertex(ele[1]), Vertex(ele[0]), ele[2])

    graph_kruskal = kruskal(graph)
    printGraph(graph_kruskal)


if __name__ == "__main__":
    main()
