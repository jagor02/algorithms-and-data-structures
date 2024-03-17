# skończone
class Element:
    def __init__(self, dane, priorytet):
        self.__dane = dane
        self.__priorytet = priorytet

    def __lt__(self, other_element):
        return self.__priorytet < other_element.__priorytet

    def __gt__(self, other_element):
        return self.__priorytet > other_element.__priorytet

    def __str__(self):
        return f"{self.__priorytet}: {self.__dane}"


class Heap:
    def __init__(self):
        self.table = []
        self.heap_len = 0

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
            while (self.left(idx) is not None and self.table[self.left(idx)] > self.table[idx])\
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


def main():
    heap = Heap()
    priorities = [7, 5, 1, 2, 5, 3, 4, 8, 9]
    string = "GRYMOTYLA"
    for i in range(len(priorities)):
        heap.enqueue(Element(string[i], priorities[i]))
    heap.print_tree(0, 0)
    heap.print_tab()
    ele = heap.dequeue()
    print(heap.peek())
    heap.print_tab()
    print(ele)
    while not heap.is_empty():
        print(heap.dequeue())
    heap.print_tab()


if __name__ == '__main__':
    main()
