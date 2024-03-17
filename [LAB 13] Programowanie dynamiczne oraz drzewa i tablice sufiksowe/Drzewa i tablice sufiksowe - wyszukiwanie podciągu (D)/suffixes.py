# skończone
from copy import deepcopy


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
        to_destory = []
        for vert, neighs in self.list.items():
            for neigh in neighs:
                if neigh == vertex:
                    to_destory.append(vert)
                    break
        for vert in to_destory:
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

    def numbering(self):
        helping_dict = {}
        num = 0
        for vert, idx in self.vertex_dict.items():
            helping_dict[vert] = Vertex(num)
            num += 1
        sub_helping_dict1 = {}
        num = 0
        for vert in self.vertex_dict.keys():
            sub_helping_dict1[helping_dict[vert]] = num
            num += 1
        self.vertex_dict = sub_helping_dict1
        sub_helping_dict2 = {}
        for vert, edges in self.list.items():
            sub_helping_edges = {}
            for sub_vert, sub_edge in edges.items():
                sub_helping_edges[helping_dict[sub_vert]] = sub_edge
            sub_helping_dict2[helping_dict[vert]] = sub_helping_edges
        self.list = sub_helping_dict2

    def get_nodes(self):
        nodes = []
        for node in self.vertex_dict.keys():
            nodes.append(node)
        return nodes


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


def sufixes_tree(S):
    len_S = len(S)
    sufixes = []
    for i in range(len_S):
        sufixes.append(S[i:])
    Trie_tree = AdjList()
    Trie_tree.insertVertex(Vertex(0))
    num = 1
    for w in sufixes:
        travelling_vertex = Vertex(0)
        len_suffix = len(w)
        i = 0
        travelled = True
        while travelled and i < len_suffix:
            travelled = False
            for vert, edge in Trie_tree.neighbours(Trie_tree.getVertexIdx(travelling_vertex)).items():
                if w[i] in edge:
                    travelling_vertex = vert
                    i += 1
                    travelled = True
                    break
        for j in range(i, len_suffix):
            Trie_tree.insertVertex(Vertex(num))
            Trie_tree.insertEdge(travelling_vertex, Vertex(num), w[j])
            travelling_vertex = Vertex(num)
            num += 1
    crossroads = [Vertex(0)]
    while crossroads:
        root = crossroads.pop(0)
        main_neigh = deepcopy(Trie_tree.neighbours(Trie_tree.getVertexIdx(root)))
        for vert, edge in main_neigh.items():
            travelling_vertex = vert
            travelled = True
            helping_string = edge[0][:]
            while travelled:
                travelled = False
                neigh = deepcopy(Trie_tree.neighbours(Trie_tree.getVertexIdx(travelling_vertex)))
                if len(neigh) == 1:
                    for v, e in neigh.items():
                        helping_string += e[0][:]
                        Trie_tree.deleteVertex(travelling_vertex)
                        travelling_vertex = v
                        travelled = True
                else:
                    if travelling_vertex not in main_neigh:
                        Trie_tree.insertEdge(root, travelling_vertex, helping_string)
                    if len(neigh) > 1:
                        crossroads.append(travelling_vertex)
    Trie_tree.numbering()
    return Trie_tree


def find_in_sufixes_tree(suf_tree, W):
    found = False
    count = 0
    len_W = len(W)
    root = Vertex(0)
    s = 0
    t = 1
    travelled = True
    travelling_vertex = root
    helping_word = ""
    while travelled:
        travelled = False
        while t < len_W:
            in_flag = False
            for vert, edge in suf_tree.neighbours(suf_tree.getVertexIdx(travelling_vertex)).items():
                if W[s:t] in edge:
                    helping_word += edge[0][:]
                    travelling_vertex = vert
                    travelled = True
                    in_flag = True
                    break
            t += 1
            if in_flag:
                s = t - 1
                break
    len_rest_word = len_W - len(helping_word)
    new_helping_word = helping_word
    for vert, edge in suf_tree.neighbours(suf_tree.getVertexIdx(travelling_vertex)).items():
        if W[len_W - len_rest_word:len_W] == edge[0][:len_rest_word]:
            new_helping_word += edge[0][:len_rest_word]
            travelling_vertex = vert
            break
    helping_word = new_helping_word
    if W == helping_word:
        found = True
        neigh = suf_tree.neighbours(suf_tree.getVertexIdx(travelling_vertex))
        if len(neigh) == 0:
            count = 1
        else:
            queue = []
            for vert in neigh.keys():
                queue.append(vert)
            while queue:
                helping_vertex = queue.pop(0)
                sub_neigh = suf_tree.neighbours(suf_tree.getVertexIdx(helping_vertex))
                if len(sub_neigh) == 0:
                    count += 1
                else:
                    for sub_vert in sub_neigh.keys():
                        queue.append(sub_vert)
    return found, count


def sufixes_table_naive(S):
    len_S = len(S)
    sufixes = []
    for i in range(len_S):
        sufixes.append(S[i:])
    sufixes_idx_table_sorted = []
    sufixes_copy = sufixes[:]
    for _ in range(len_S):
        alphabetic_min = sufixes_copy[0]
        for word in sufixes_copy:
            if word == alphabetic_min:
                continue
            i = 0
            flag = True
            alphabetic_min_len = len(alphabetic_min)
            word_len = len(word)
            while flag and (alphabetic_min_len > i and word_len > i):
                if alphabetic_min[i] > word[i] or word_len <= i:
                    alphabetic_min = word
                    flag = False
                elif alphabetic_min[i] < word[i] or alphabetic_min_len <= i:
                    flag = False
                else:
                    i += 1
        sufixes_idx_table_sorted.append(sufixes.index(alphabetic_min))
        sufixes_copy.remove(alphabetic_min)
    return sufixes_idx_table_sorted, sufixes


def find_in_sufixes_table(suf_table, table_of_sufixes, W):
    sorted_sufixes = []
    for i in suf_table:
        sorted_sufixes.append(table_of_sufixes[i])
    l = 0
    p = len(sorted_sufixes)-1
    found = False
    while p >= l and not found:
        s = (l + p) // 2
        suf = sorted_sufixes[s]
        flag = True
        i = 0
        while flag:
            if suf[i] == W[i]:
                if i == len(W) - 1:
                    found = True
                    break
                i += 1
                continue
            elif suf[i] > W[i] or len(W) <= i:
                flag = False
                p = s - 1
            elif suf[i] < W[i] or len(suf) <= i:
                flag = False
                l = s + 1
    return found


def sufixes_table_from_sufixes_tree(S):
    suf_table = []
    len_S = len(S)
    sufixes = []
    for i in range(len_S):
        sufixes.append(S[i:])
    suf_tree = sufixes_tree(S)
    visited = {}
    nodes = suf_tree.get_nodes()
    for node in nodes:
        visited[node] = False
    stack = [(nodes[0], "")]
    visited[nodes[0]] = True
    while stack:
        to_check = []
        nodedge = stack.pop()
        neigh = suf_tree.neighbours(suf_tree.getVertexIdx(nodedge[0]))
        if len(neigh) == 0:
            suf_table.insert(0, (sufixes.index(nodedge[1])))
        for node, edge in neigh.items():
            if not visited[node]:
                to_check.append((node, nodedge[1]+edge[0]))
        for _ in range(len(to_check)):
            alphabetic_min = to_check[0]
            for word in to_check:
                if word[1] == alphabetic_min[1]:
                    continue
                i = 0
                flag = True
                alphabetic_min_len = len(alphabetic_min[1])
                word_len = len(word[1])
                while flag and (alphabetic_min_len > i and word_len > i):
                    if alphabetic_min[1][i] > word[1][i] or word_len <= i:
                        alphabetic_min = word
                        flag = False
                    elif alphabetic_min[1][i] < word[1][i] or alphabetic_min_len <= i:
                        flag = False
                    else:
                        i += 1
            stack.append(alphabetic_min)
            visited[alphabetic_min[0]] = True
            to_check.remove(alphabetic_min)
    return suf_table, sufixes


def main():
    S = "banana\0"
    print(f"Przeszukiwany tekst: {S}")

    suf_tree = sufixes_tree(S)
    print("Drzewo sufiksowe dla przeszukiwanego tekstu")
    printGraph(suf_tree)

    W = "ban"
    found, count = find_in_sufixes_tree(suf_tree, W)
    print(f"Wzór: {W}")
    print(f"Znaleziono: {found}; Ile: {count}")

    W = "kan"
    found, count = find_in_sufixes_tree(suf_tree, W)
    print(f"Wzór: {W}")
    print(f"Znaleziono: {found}; Ile: {count}")

    W = "na"
    found, count = find_in_sufixes_tree(suf_tree, W)
    print(f"Wzór: {W}")
    print(f"Znaleziono: {found}; Ile: {count}")

    sufixes_table, sufixes = sufixes_table_naive(S)
    print("Tablica sufiksowa dla przeszukiwanego tekstu (metoda naiwna):")
    print(sufixes_table)

    W = "ban"
    found = find_in_sufixes_table(sufixes_table, sufixes, W)
    print(f"Wzór: {W}")
    print(f"Znaleziono: {found}")

    W = "kan"
    found = find_in_sufixes_table(sufixes_table, sufixes, W)
    print(f"Wzór: {W}")
    print(f"Znaleziono: {found}")

    W = "na"
    found = find_in_sufixes_table(sufixes_table, sufixes, W)
    print(f"Wzór: {W}")
    print(f"Znaleziono: {found}")

    sufixes_table, sufixes = sufixes_table_from_sufixes_tree(S)
    print("Tablica sufiksowa dla przeszukiwanego tekstu (na podstawie drzewa sufiksowego):")
    print(sufixes_table)

    W = "ban"
    found = find_in_sufixes_table(sufixes_table, sufixes, W)
    print(f"Wzór: {W}")
    print(f"Znaleziono: {found}")

    W = "kan"
    found = find_in_sufixes_table(sufixes_table, sufixes, W)
    print(f"Wzór: {W}")
    print(f"Znaleziono: {found}")

    W = "na"
    found = find_in_sufixes_table(sufixes_table, sufixes, W)
    print(f"Wzór: {W}")
    print(f"Znaleziono: {found}")


if __name__ == "__main__":
    main()
