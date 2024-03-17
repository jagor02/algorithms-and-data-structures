# skończone
import time


def string_compare(P, T, i, j):
    if i == 0:
        return j
    if j == 0:
        return i
    change = string_compare(P, T, i-1, j-1) + int(P[i] != T[j])
    add = string_compare(P, T, i, j-1) + 1
    delete = string_compare(P, T, i-1, j) + 1
    min_cost = min(change, add, delete)
    return min_cost


def PD(P, T):
    D = [[0 for _ in range(len(T))] for _ in range(len(P))]
    D[0] = [i for i in range(len(T))]
    for i in range(1, len(P)):
        D[i][0] = i
    parent = [['X' for _ in range(len(T))] for _ in range(len(P))]
    for i in range(1, len(T)):
        parent[0][i] = 'I'
    for i in range(1, len(P)):
        parent[i][0] = 'D'
    for i in range(1, len(P)):
        for j in range(1, len(T)):
            change = D[i - 1][j - 1] + int(P[i] != T[j])
            add = D[i][j - 1] + 1
            delete = D[i - 1][j] + 1
            min_cost = min(change, add, delete)
            D[i][j] = min_cost
            if change == min_cost:
                if P[i] != T[j]:
                    parent[i][j] = 'S'
                else:
                    parent[i][j] = 'M'
            elif add == min_cost:
                parent[i][j] = 'I'
            elif delete == min_cost:
                parent[i][j] = 'D'
    return D[len(P)-1][len(T)-1], parent


def path_reconstruction(P, T):
    _, parent = PD(P, T)
    i = len(P)-1
    j = len(T)-1
    operations = []
    while parent[i][j] != 'X':
        operations.append(parent[i][j])
        if parent[i][j] == 'M' or parent[i][j] == 'S':
            i -= 1
            j -= 1
        elif parent[i][j] == 'I':
            j -= 1
        elif parent[i][j] == 'D':
            i -= 1
    operations = operations[::-1]
    string = ""
    for op in operations:
        string += op
    return string


def match(P, T):
    D = [[0 for _ in range(len(T))] for _ in range(len(P))]
    for i in range(1, len(P)):
        D[i][0] = i
    parent = [['X' for _ in range(len(T))] for _ in range(len(P))]
    for i in range(1, len(P)):
        parent[i][0] = 'D'
    for i in range(1, len(P)):
        for j in range(1, len(T)):
            change = D[i - 1][j - 1] + int(P[i] != T[j])
            add = D[i][j - 1] + 1
            delete = D[i - 1][j] + 1
            min_cost = min(change, add, delete)
            D[i][j] = min_cost
            if change == min_cost:
                if P[i] != T[j]:
                    parent[i][j] = 'S'
                else:
                    parent[i][j] = 'M'
            elif add == min_cost:
                parent[i][j] = 'I'
            elif delete == min_cost:
                parent[i][j] = 'D'
    i = len(P) - 1
    j = 0
    for k in range(1, len(T)):
        if D[i][k] < D[i][j]:
            j = k
    return D[len(P)-1][len(T)-1], j


def max_mutual_seq(P, T):
    D = [[0 for _ in range(len(T))] for _ in range(len(P))]
    D[0] = [i for i in range(len(T))]
    for i in range(1, len(P)):
        D[i][0] = i
    parent = [['X' for _ in range(len(T))] for _ in range(len(P))]
    for i in range(1, len(T)):
        parent[0][i] = 'I'
    for i in range(1, len(P)):
        parent[i][0] = 'D'
    for i in range(1, len(P)):
        for j in range(1, len(T)):
            change = D[i - 1][j - 1] + (100 if P[i] != T[j] else 0)
            add = D[i][j - 1] + 1
            delete = D[i - 1][j] + 1
            min_cost = min(change, add, delete)
            D[i][j] = min_cost
            if change == min_cost:
                if P[i] != T[j]:
                    parent[i][j] = 'S'
                else:
                    parent[i][j] = 'M'
            elif add == min_cost:
                parent[i][j] = 'I'
            else:
                parent[i][j] = 'D'
    num = 0
    coords = []
    ret_string = ""
    for i in range(len(P)):
        for j in range(len(T)):
            if parent[i][j] == 'M':
                num += 1
                coords.append((i, j))
    for e in range(num):
        y, x = coords[e]
        string = "" + P[y]
        ii = y
        jj = x
        i = y
        while i < len(P):
            j = jj
            while j < len(T):
                if parent[i][j] == 'M':
                    if j > jj and i > ii:
                        string += P[i]
                        jj = j
                        ii = i
                j += 1
            i += 1
        if len(string) > len(ret_string):
            ret_string = string
    return ret_string


def selection_sort_swap(table):
    table_len = len(table)
    for i in range(table_len):
        t_m = table[i]
        m = i
        for j in range(i+1, table_len):
            if table[j] < t_m:
                t_m = table[j]
                m = j
        table[i], table[m] = table[m], table[i]


def main():
    # P = ' kot'
    # T = ' koń'

    # t_start = time.perf_counter()
    # min_cost = string_compare(P, T, len(P)-1, len(T)-1)
    # t_stop = time.perf_counter()
    # print("Czas obliczeń:", "{:.7f}".format(t_stop - t_start))

    # print(min_cost)

    P = ' kot'
    T = ' pies'

    # t_start = time.perf_counter()
    min_cost = string_compare(P, T, len(P)-1, len(T)-1)
    # t_stop = time.perf_counter()
    # print("Czas obliczeń:", "{:.7f}".format(t_stop - t_start))

    print(min_cost)

    # P = ' biały autobus'
    # T = ' czarny autokar'

    # t_start = time.perf_counter()
    # min_cost = string_compare(P, T, len(P)-1, len(T)-1)
    # t_stop = time.perf_counter()
    # print("Czas obliczeń:", "{:.7f}".format(t_stop - t_start))

    # print(min_cost)

    # P = ' kot'
    # T = ' koń'

    # t_start = time.perf_counter()
    # min_cost, _ = PD(P, T)
    # t_stop = time.perf_counter()
    # print("Czas obliczeń:", "{:.7f}".format(t_stop - t_start))

    # print(min_cost)

    # P = ' kot'
    # T = ' pies'

    # t_start = time.perf_counter()
    # min_cost, _ = PD(P, T)
    # t_stop = time.perf_counter()
    # print("Czas obliczeń:", "{:.7f}".format(t_stop - t_start))

    # print(min_cost)

    P = ' biały autobus'
    T = ' czarny autokar'

    # t_start = time.perf_counter()
    min_cost, _ = PD(P, T)
    # t_stop = time.perf_counter()
    # print("Czas obliczeń:", "{:.7f}".format(t_stop - t_start))

    print(min_cost)

    P = ' thou shalt not'
    T = ' you should not'

    print(path_reconstruction(P, T))

    P = ' ban'
    T = ' mokeyssbanana'

    _, idx = match(P, T)
    print(idx - len(P) + 2)

    P = ' bin'
    T = ' mokeyssbanana'

    _, idx = match(P, T)
    print(idx - len(P) + 2)

    P = ' democrat'
    T = ' republican'

    string = max_mutual_seq(P, T)
    print(string)

    T = ' 243517698'
    P_table = [int(ele) for ele in T if ele != ' ']
    selection_sort_swap(P_table)
    P = " "
    for ele in P_table:
        P += str(ele)

    string = max_mutual_seq(P, T)
    print(string)


if __name__ == "__main__":
    main()
