# skończone
import random
import time


class Element:
    def __init__(self, dane, priorytet):
        self.__dane = dane
        self.__priorytet = priorytet

    def __lt__(self, other_element):
        return self.__priorytet < other_element.__priorytet

    def __gt__(self, other_element):
        return self.__priorytet > other_element.__priorytet

    def __repr__(self):
        return f"{self.__priorytet}: {self.__dane}"


class Heap:
    def __init__(self, table=None):
        if table is None:
            self.table = []
            self.heap_len = 0
        else:
            self.table = table
            self.heap_len = len(table)
            for i in range((self.heap_len - 2) // 2, -1, -1):
                self.heap_condition(i)

    def is_empty(self):
        return self.heap_len == 0

    def peek(self):
        return None if self.is_empty() else self.table[0]

    def dequeue(self):
        if self.is_empty():
            return None
        else:
            self.table[0], self.table[self.heap_len - 1] = self.table[self.heap_len - 1], self.table[0]
            self.heap_len -= 1
            self.heap_condition(0)
            return self.table[self.heap_len]

    def enqueue(self, element):
        if self.heap_len == len(self.table):
            self.table.append(element)
        elif self.heap_len < len(self.table):
            self.table[self.heap_len] = element
        self.heap_len += 1
        idx = self.heap_len - 1
        while self.parent(idx) is not None and self.table[self.parent(idx)] < self.table[idx]:
            self.table[idx], self.table[self.parent(idx)] = self.table[self.parent(idx)], self.table[idx]
            idx = self.parent(idx)

    def left(self, idx):
        if idx + 1 > self.heap_len or idx < 0:
            return None
        n_idx = 2 * idx + 1
        if not n_idx + 1 > self.heap_len:
            return n_idx
        else:
            return None

    def right(self, idx):
        if idx + 1 > self.heap_len or idx < 0:
            return None
        n_idx = 2 * idx + 2
        if not n_idx + 1 > self.heap_len:
            return n_idx
        else:
            return None

    def parent(self, idx):
        if idx + 1 > self.heap_len or idx < 0:
            return None
        n_idx = (idx - 1) // 2
        if not n_idx < 0:
            return n_idx
        else:
            return None

    def heap_condition(self, idx):
        if not (idx + 1 > self.heap_len or idx < 0):
            while (self.left(idx) is not None and self.right(idx) is not None and self.table[self.left(idx)] >
                   self.table[idx]) or (self.right(idx) is not None and self.table[self.right(idx)] > self.table[idx]):
                if self.table[self.left(idx)] > self.table[self.right(idx)]:
                    self.table[idx], self.table[self.left(idx)] = self.table[self.left(idx)], self.table[idx]
                    idx = self.left(idx)
                else:
                    self.table[idx], self.table[self.right(idx)] = self.table[self.right(idx)], self.table[idx]
                    idx = self.right(idx)

    def print_tab(self):
        print('{', end=' ')
        print(*self.table[:self.heap_len], sep=', ', end=' ')
        print('}')

    def print_tree(self, idx, lvl):
        if idx is not None and idx < len(self.table):
            self.print_tree(self.right(idx), lvl + 1)
            print(2 * lvl * '  ', self.table[idx] if self.table[idx] else None)
            self.print_tree(self.left(idx), lvl + 1)


def insertion_sort(table):
    for i in range(1, len(table)):
        buffor = table[i]
        flag = False
        for j in range(i - 1, -1, -1):
            if table[j] > buffor:
                table[j + 1] = table[j]
            else:
                table[j + 1] = buffor
                flag = True
                break
        if not flag:
            table[0] = buffor


def Shell(table):
    tab_len = len(table)
    k = 2
    while (3**k-1)/2 < tab_len/3:
        k += 1
    h = int((3**(k-1)-1)/2)
    while h > 0:
        for i in range(h, tab_len):
            for j in range(i, -1, -h):
                k = j-h
                if k >= 0 and table[k] > table[j]:
                    table[k], table[j] = table[j], table[k]
                else:
                    break
        h = h//3


def main():
    list_ele_inser = [(5, 'A'), (5, 'B'), (7, 'C'), (2, 'D'), (5, 'E'), (1, 'F'), (7, 'G'), (5, 'H'), (1, 'I'),
                      (2, 'J')]
    list_of_element_inser = []
    for ele in list_ele_inser:
        list_of_element_inser.append(Element(ele[1], ele[0]))
    insertion_sort(list_of_element_inser)
    print(list_of_element_inser)
    print("Sortowanie przez wstawianie jest stabilne.")

    list_ele_Shell = [(5, 'A'), (5, 'B'), (7, 'C'), (2, 'D'), (5, 'E'), (1, 'F'), (7, 'G'), (5, 'H'),
                      (1, 'I'), (2, 'J')]
    list_of_element_Shell = []
    for ele in list_ele_Shell:
        list_of_element_Shell.append(Element(ele[1], ele[0]))
    Shell(list_of_element_Shell)
    print(list_of_element_Shell)
    print("Sortowanie metodą Shella jest stabilne.")

    list_num_inser = [int(random.random() * 100) for _ in range(10000)]
    t_start_inser = time.perf_counter()
    insertion_sort(list_num_inser)
    t_stop_inser = time.perf_counter()
    print("Czas obliczeń sortowania przez wstawianie wynosi:", "{:.7f}".format(t_stop_inser - t_start_inser))

    list_num_Shell = [int(random.random() * 100) for _ in range(10000)]
    t_start_Shell = time.perf_counter()
    Shell(list_num_Shell)
    t_stop_Shell = time.perf_counter()
    print("Czas obliczeń sortowania metodą Shella wynosi:", "{:.7f}".format(t_stop_Shell - t_start_Shell))

    list_num_heap = [int(random.random() * 100) for _ in range(10000)]
    t_start_heap = time.perf_counter()
    heap_num_heap = Heap(list_num_heap)
    while not heap_num_heap.is_empty():
        heap_num_heap.dequeue()
    t_stop_heap = time.perf_counter()
    print("Czas obliczeń sortowania przez kopcowanie wynosi:", "{:.7f}".format(t_stop_heap - t_start_heap))


if __name__ == "__main__":
    main()
