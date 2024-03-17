# skończone
import cv2
import numpy as np
import matplotlib.pyplot as plt


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
    return parent, visited


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
    parent, _ = BFS(graph, start_vertex)
    min_capacity = max_flow(graph, start_vertex, stop_vertex, parent)
    while min_capacity > 0:
        augmentation(graph, start_vertex, stop_vertex, parent, min_capacity)
        parent, _ = BFS(graph, start_vertex)
        min_capacity = max_flow(graph, start_vertex, stop_vertex, parent)
    for n, e in graph.neighbours(graph.getVertexIdx(stop_vertex)).items():
        for edge in e:
            if edge.isResidual is True:
                for e_reverse in graph.neighbours(graph.getVertexIdx(n))[stop_vertex]:
                    if edge.capacity == e_reverse.capacity and edge.isResidual != e_reverse.isResidual:
                        flow_sum += e_reverse.flow
                        break
    return flow_sum


def min_cut(graph):
    min_cut_edges = []
    parent = BFS(graph, Vertex('s'))
    for idx in range(len(parent)):
        if parent[idx] is not None or graph.getVertex(idx) == Vertex('s'):
            for neigh, edges in graph.neighbours(idx).items():
                for edge in edges:
                    if edge.isResidual is False and edge.residual == 0 and parent[graph.getVertexIdx(neigh)] is None:
                        min_cut_edges.append(edge)
                        

def BFS_copy(graph, start_vertex):
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
                    if not edge.isResidual and edge.residual > 0:
                        queue.append(n_idx)
                        visited[n_idx] = True
                        parent[n_idx] = graph.getVertex(vert_idx)
                        break
    return parent, visited


def main():
    I = cv2.imread("min_cut_seg_1.png", cv2.IMREAD_GRAYSCALE)
    
    (Y, X) = I.shape
    
    scrible_FG = np.zeros((Y,X),dtype=np.ubyte)
    scrible_FG[100:120, 100:120] = 255

    scrible_BG = np.zeros((Y,X),dtype=np.ubyte)
    scrible_BG[0:20, 0:20] = 255

    I = cv2.resize(I,(32,32))
    scrible_BG = cv2.resize(scrible_BG,(32,32))
    scrible_FG = cv2.resize(scrible_FG,(32,32))
    
    hist_FG = cv2.calcHist([I],[0],scrible_FG,[256],[0,256])
    hist_FG = hist_FG/sum(hist_FG)
    
    plt.imshow(scrible_FG, 'gray')
    plt.show()
    
    for i in range(256):
        print(i, hist_FG[i])

    hist_BG = cv2.calcHist([I],[0],scrible_BG,[256],[0,256])
    hist_BG = hist_BG/sum(hist_BG)
    
    (YY, XX) = I.shape  
    
    graph = AdjList()
    
    graph.insertVertex(Vertex('s'))
    graph.insertVertex(Vertex('t'))
    for y in range(YY):
        for x in range(XX):
            graph.insertVertex(Vertex(XX * y + x))   
            
    for y in range(YY):
        for x in range(XX):
            if y == 0 and x == 0:
                for j in range(0, 2):
                    for i in range(0, 2):
                        if not (j == 0 and i == 0):
                            graph.insertEdge(Vertex(XX * 0 + 0), Vertex(XX * j + i), Edge(np.exp((-1/2)*np.abs(I[0, 0]-I[j, i])), False))
                            graph.insertEdge(Vertex(XX * j + i), Vertex(XX * 0 + 0), Edge(np.exp((-1/2)*np.abs(I[0, 0]-I[j, i])), True))
            elif y == YY - 1 and x == 0:
                for j in range(YY - 2, YY):
                    for i in range(0, 2):
                        if not (j == YY - 1 and i == 0):
                            graph.insertEdge(Vertex(XX * (YY - 1) + 0), Vertex(XX * j + i), Edge(np.exp((-1/2)*np.abs(I[(YY-1), 0]-I[j, i])), False))
                            graph.insertEdge(Vertex(XX * j + i), Vertex(XX * (YY - 1) + 0), Edge(np.exp((-1/2)*np.abs(I[(YY-1), 0]-I[j, i])), True))
            elif y == 0 and x == XX - 1:
                for j in range(0, 2):
                    for i in range(XX - 2, XX):
                        if not (j == 0 and i == XX - 1):
                            graph.insertEdge(Vertex(XX * 0 + (XX - 1)), Vertex(XX * j + i), Edge(np.exp((-1/2)*np.abs(I[0, (XX - 1)]-I[j, i])), False))
                            graph.insertEdge(Vertex(XX * j + i), Vertex(XX * 0 + (XX - 1)), Edge(np.exp((-1/2)*np.abs(I[0, (XX - 1)]-I[j, i])), True))
            elif y == YY - 1 and x == XX - 1:
                for j in range(YY - 2, YY):
                    for i in range(XX - 2, XX):
                        if not (j == YY - 1 and i == XX - 1):
                            graph.insertEdge(Vertex(XX * (YY - 1) + (XX - 1)), Vertex(XX * j + i),
                                             Edge(np.exp((-1/2)*np.abs(I[(YY-1), (XX - 1)]-I[j, i])), False))
                            graph.insertEdge(Vertex(XX * j + i), Vertex(XX * (YY - 1) + (XX - 1)),
                                             Edge(np.exp((-1/2)*np.abs(I[(YY-1), (XX - 1)]-I[j, i])), True))
            elif y == 0:
                for j in range(0, 2):
                    for i in range(x - 1, x + 2):
                        if not (j == 0 and i == x):
                            graph.insertEdge(Vertex(XX * 0 + x), Vertex(XX * j + i), Edge(np.exp((-1/2)*np.abs(I[0, x]-I[j, i])), False))
                            graph.insertEdge(Vertex(XX * j + i), Vertex(XX * 0 + x), Edge(np.exp((-1/2)*np.abs(I[0, x]-I[j, i])), True))
            elif y == YY - 1:
                for j in range(YY - 2, YY):
                    for i in range(x - 1, x + 2):
                        if not (j == YY - 1 and i == x):
                            graph.insertEdge(Vertex(XX * (YY - 1) + x), Vertex(XX * j + i), Edge(np.exp((-1/2)*np.abs(I[(YY-1), x]-I[j, i])), False))
                            graph.insertEdge(Vertex(XX * j + i), Vertex(XX * (YY - 1) + x), Edge(np.exp((-1/2)*np.abs(I[(YY-1), x]-I[j, i])), True))
            elif x == 0:
                for j in range(y - 1, y + 2):
                    for i in range(0, 2):
                        if not (j == y and i == 0):
                            graph.insertEdge(Vertex(XX * y + 0), Vertex(XX * j + i), Edge(np.exp((-1/2)*np.abs(I[y, 0]-I[j, i])), False))
                            graph.insertEdge(Vertex(XX * j + i), Vertex(XX * y + 0), Edge(np.exp((-1/2)*np.abs(I[y, 0]-I[j, i])), True))
            elif x == XX - 1:
                for j in range(y - 1, y + 2):
                    for i in range(XX - 2, XX):
                        if not (j == y and i == XX - 1):
                            graph.insertEdge(Vertex(XX * y + (XX - 1)), Vertex(XX * j + i), Edge(np.exp((-1/2)*np.abs(I[y, (XX-1)]-I[j, i])), False))
                            graph.insertEdge(Vertex(XX * j + i), Vertex(XX * y + (XX - 1)), Edge(np.exp((-1/2)*np.abs(I[y, (XX-1)]-I[j, i])), True))
            else:
                for j in range(y - 1, y + 2):
                    for i in range(x - 1, x + 2):
                        if not (j == y and i == x):
                            graph.insertEdge(Vertex(XX * y + x), Vertex(XX * j + i), Edge(np.exp((-1/2)*np.abs(I[y, x]-I[j, i])), False))
                            graph.insertEdge(Vertex(XX * j + i), Vertex(XX * y + x), Edge(np.exp((-1/2)*np.abs(I[y, x]-I[j, i])), True))
    
    I_max = (I.max()).astype('int16')
    I_min = (I.min()).astype('int16')
    
    I_avg = ((I_max+I_min)/2).astype('uint8')
    
    for y in range(YY):
        for x in range(XX):
            if scrible_FG[y, x] == 255:
                graph.insertEdge(Vertex('s'), Vertex(XX * y + x), Edge(np.inf, False))
                graph.insertEdge(Vertex(XX * y + x), Vertex('s'), Edge(np.inf, True))
            elif scrible_BG[y, x] == 255:
                graph.insertEdge(Vertex('s'), Vertex(XX * y + x), Edge(0, False))
                graph.insertEdge(Vertex(XX * y + x), Vertex('s'), Edge(0, True))
            else:
                graph.insertEdge(Vertex('s'), Vertex(XX * y + x), Edge(hist_FG[I[y, x]], False))
                graph.insertEdge(Vertex(XX * y + x), Vertex('s'), Edge(hist_FG[I[y, x]], True))
                
    for y in range(YY):
        for x in range(XX):
            if scrible_FG[y, x] == 255:
                graph.insertEdge(Vertex('t'), Vertex(XX * y + x), Edge(0, True))
                graph.insertEdge(Vertex(XX * y + x), Vertex('t'), Edge(0, False))
            elif scrible_BG[y, x] == 255:
                graph.insertEdge(Vertex('t'), Vertex(XX * y + x), Edge(np.inf, True))
                graph.insertEdge(Vertex(XX * y + x), Vertex('t'), Edge(np.inf, False))
            else:
                graph.insertEdge(Vertex('t'), Vertex(XX * y + x), Edge(hist_BG[I[y, x]], True))
                graph.insertEdge(Vertex(XX * y + x), Vertex('t'), Edge(hist_BG[I[y, x]], False))
                    
    p = ford_fulkerson(graph, Vertex('s'), Vertex('t'))
    
    parent, visited = BFS_copy(graph, Vertex('s'))
    
    m = max_flow(graph, Vertex('s'), Vertex('t'), parent)
    
    print(visited)
    
    
                
if __name__ == "__main__":
    main()