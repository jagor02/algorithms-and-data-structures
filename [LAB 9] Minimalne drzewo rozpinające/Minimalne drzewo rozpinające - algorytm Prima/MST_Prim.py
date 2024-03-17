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
                edge_table.append((vert.key, v.key))
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


def main():
    graph = AdjList()

    existing_vertex = []

    for ele in graf_mst.graf:
        if ele[0] not in existing_vertex:
            graph.insertVertex(ele[0])
            existing_vertex.append(ele[0])
        if ele[1] not in existing_vertex:
            graph.insertVertex(ele[1])
            existing_vertex.append(ele[1])
        graph.insertEdge(ele[0], ele[1], ele[2])
        graph.insertEdge(ele[1], ele[0], ele[2])

    printGraph(Prim(graph, 0)[0])


if __name__ == "__main__":
    main()
