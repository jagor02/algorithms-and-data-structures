# skończone
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
    def __init__(self, capacity, isResidual):
        self.capacity = capacity
        self.isResidual = isResidual
        if self.isResidual:
            self.flow = None
            self.residual = 0
        else:
            self.flow = 0
            self.residual = self.capacity

    def __repr__(self):
        return f"{self.capacity} {self.flow} {self.residual} {self.isResidual}"

    def __eq__(self, other_edge):
        return self.capacity == other_edge.capacity


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
        flag = False
        for v in self.list[vertex1].keys():
            if v == vertex2:
                flag = True
                break
        if flag:
            (self.list[vertex1])[vertex2].append(edge)
        else:
            (self.list[vertex1])[vertex2] = [edge]

    def deleteVertex(self, vertex):
        for vert in self.neighbours(self.getVertexIdx(vertex)):
            del self.list[vert][vertex]
        del self.list[vertex]
        del self.vertex_dict[vertex]

    def deleteEdge(self, vertex1, vertex2, edge):
        edge_idx = 0
        for e in (self.list[vertex1])[vertex2]:
            if e == edge:
                del ((self.list[vertex1])[vertex2])[edge_idx]
            else:
                edge_idx += 1
        edge_idx = 0
        for e in (self.list[vertex2])[vertex1]:
            if e == edge:
                del ((self.list[vertex2])[vertex1])[edge_idx]
            else:
                edge_idx += 1

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


def BFS(graph, start_vertex):
    visited = [False for _ in range(graph.order())]
    parent = [None for _ in range(graph.order())]
    start_vertex_idx = graph.getVertexIdx(start_vertex)
    queue = [start_vertex_idx]
    visited[start_vertex_idx] = True
    while queue:
        vert_idx = queue.pop(0)
        neigh = graph.neighbours(vert_idx)
        for n, e in neigh.items():
            n_idx = graph.getVertexIdx(n)
            if visited[n_idx] is False:
                for edge in e:
                    if edge.residual > 0:
                        queue.append(n_idx)
                        visited[n_idx] = True
                        parent[n_idx] = graph.getVertex(vert_idx)
                        break
    return parent


def max_flow(graph, start_vertex, stop_vertex, parent):
    actual_vert_idx = graph.getVertexIdx(stop_vertex)
    min_capacity = float('inf')
    if parent[actual_vert_idx] is None:
        return 0
    else:
        while actual_vert_idx != graph.getVertexIdx(start_vertex):
            for n, e in graph.neighbours(graph.getVertexIdx(parent[actual_vert_idx])).items():
                if graph.getVertexIdx(n) == actual_vert_idx:
                    for edge in e:
                        if edge.isResidual is False:
                            if edge.residual < min_capacity:
                                min_capacity = edge.residual
            actual_vert_idx = graph.getVertexIdx(parent[actual_vert_idx])
    return min_capacity


def augmentation(graph, start_vertex, stop_vertex, parent, min_capacity):
    actual_vert_idx = graph.getVertexIdx(stop_vertex)
    while actual_vert_idx != graph.getVertexIdx(start_vertex):
        for n, e in graph.neighbours(graph.getVertexIdx(parent[actual_vert_idx])).items():
            if graph.getVertexIdx(n) == actual_vert_idx:
                for edge in e:
                    for e_reverse in graph.neighbours(actual_vert_idx)[parent[actual_vert_idx]]:
                        if edge.capacity == e_reverse.capacity and edge.isResidual != e_reverse.isResidual:
                            if edge.isResidual is False:
                                edge.flow += min_capacity
                                edge.residual -= min_capacity
                                e_reverse.residual += min_capacity
                                break
                            else:
                                e_reverse.flow += min_capacity
                                e_reverse.residual -= min_capacity
                                edge.residual += min_capacity
                                break
        actual_vert_idx = graph.getVertexIdx(parent[actual_vert_idx])


def ford_fulkerson(graph, start_vertex, stop_vertex):
    flow_sum = 0
    parent = BFS(graph, start_vertex)
    min_capacity = max_flow(graph, start_vertex, stop_vertex, parent)
    while min_capacity > 0:
        augmentation(graph, start_vertex, stop_vertex, parent, min_capacity)
        parent = BFS(graph, start_vertex)
        min_capacity = max_flow(graph, start_vertex, stop_vertex, parent)
    for n, e in graph.neighbours(graph.getVertexIdx(stop_vertex)).items():
        for edge in e:
            if edge.isResidual is True:
                for e_reverse in graph.neighbours(graph.getVertexIdx(n))[stop_vertex]:
                    if edge.capacity == e_reverse.capacity and edge.isResidual != e_reverse.isResidual:
                        flow_sum += e_reverse.flow
                        break
    return flow_sum


def main():
    graf_0 = [('s', 'u', 2), ('u', 't', 1), ('u', 'v', 3), ('s', 'v', 1), ('v', 't', 2)]
    graf_1 = [('s', 'a', 16), ('s', 'c', 13), ('a', 'c', 10), ('c', 'a', 4), ('a', 'b', 12), ('b', 'c', 9),
              ('b', 't', 20), ('c', 'd', 14), ('d', 'b', 7), ('d', 't', 4)]
    graf_2 = [('s', 'a', 3), ('s', 'c', 3), ('a', 'b', 4), ('b', 's', 3), ('b', 'c', 1), ('b', 'd', 2), ('c', 'e', 6),
              ('c', 'd', 2), ('d', 't', 1), ('e', 't', 9)]
    graf_3 = [('s', 'a', 8), ('s', 'd', 3), ('a', 'b', 9), ('b', 'd', 7), ('b', 't', 2), ('c', 't', 5), ('d', 'b', 7),
              ('d', 'c', 4)]
    grafy = [graf_0, graf_1, graf_2, graf_3]
    for graf in grafy:
        graph = AdjList()
        existing_vertexes = []
        for ele in graf:
            v1 = Vertex(ele[0])
            if v1 not in existing_vertexes:
                graph.insertVertex(v1)
                existing_vertexes.append(v1)
            v2 = Vertex(ele[1])
            if v2 not in existing_vertexes:
                graph.insertVertex(v2)
                existing_vertexes.append(v2)
            graph.insertEdge(v1, v2, Edge(ele[2], isResidual=False))
            graph.insertEdge(v2, v1, Edge(ele[2], isResidual=True))
        ford_fulkerson_graph = ford_fulkerson(graph, Vertex('s'), Vertex('t'))
        print(ford_fulkerson_graph)
        printGraph(graph)


if __name__ == "__main__":
    main()
