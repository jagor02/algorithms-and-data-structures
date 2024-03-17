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
            while (self.left(idx) is not None and self.right(idx) is not None and self.table[self.left(idx)] > self.table[idx]) \
                    or (self.right(idx) is not None and self.table[self.right(idx)] > self.table[idx]):
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
        
def selection_sort_shift(table):
    table_len = len(table)
    for i in range(table_len):
        t_m = table[i]
        m = i
        for j in range(i+1, table_len):
            if table[j] < t_m:
                t_m = table[j]
                m = j
        table.insert(i, table.pop(m))

def main():
    list_ele_heap = [(5, 'A'), (5, 'B'), (7, 'C'), (2, 'D'), (5, 'E'), (1, 'F'), (7, 'G'), (5, 'H'), (1, 'I'), (2, 'J')]
    list_of_element_heap = []
    for ele in list_ele_heap:
        list_of_element_heap.append(Element(ele[1], ele[0]))
    heap_heap = Heap(list_of_element_heap)
    heap_heap.print_tab()
    heap_heap.print_tree(0, 0)
    while not heap_heap.is_empty():
        heap_heap.dequeue()
    print(heap_heap.table)
    print("Sortowanie przez kopcowanie nie jest stabilne.")

    list_num_heap = [int(random.random() * 100) for _ in range(10000)]
    t_start_heap = time.perf_counter()
    heap_num_heap = Heap(list_num_heap)
    while not heap_num_heap.is_empty():
        heap_num_heap.dequeue()
    t_stop_heap = time.perf_counter()
    print("Czas obliczeń:", "{:.7f}".format(t_stop_heap - t_start_heap))
    
    list_ele_swap = [(5, 'A'), (5, 'B'), (7, 'C'), (2, 'D'), (5, 'E'), (1, 'F'), (7, 'G'), (5, 'H'), (1, 'I'), (2, 'J')]
    list_of_element_swap = []
    for ele in list_ele_swap:
        list_of_element_swap.append(Element(ele[1], ele[0]))
    selection_sort_swap(list_of_element_swap)
    print(list_of_element_swap)
    print("Sortowanie przez wybieranie (swap) nie jest stabilne.")
    
    list_num_swap = [int(random.random() * 100) for _ in range(10000)]
    t_start_swap = time.perf_counter()
    selection_sort_swap(list_num_swap)
    t_stop_swap = time.perf_counter()
    print("Czas obliczeń:", "{:.7f}".format(t_stop_swap - t_start_swap))
    
    list_ele_shift = [(5, 'A'), (5, 'B'), (7, 'C'), (2, 'D'), (5, 'E'), (1, 'F'), (7, 'G'), (5, 'H'), (1, 'I'), (2, 'J')]
    list_of_element_shift = []
    for ele in list_ele_shift:
        list_of_element_shift.append(Element(ele[1], ele[0]))
    selection_sort_shift(list_of_element_shift)
    print(list_of_element_shift)
    print("Sortowanie przez wybieranie (shift) jest stabilne.")
    
    list_num_shift = [int(random.random() * 100) for _ in range(10000)]
    t_start_shift = time.perf_counter()
    selection_sort_shift(list_num_shift)
    t_stop_shift = time.perf_counter()
    print("Czas obliczeń:", "{:.7f}".format(t_stop_shift - t_start_shift))


if __name__ == '__main__':
    main()
