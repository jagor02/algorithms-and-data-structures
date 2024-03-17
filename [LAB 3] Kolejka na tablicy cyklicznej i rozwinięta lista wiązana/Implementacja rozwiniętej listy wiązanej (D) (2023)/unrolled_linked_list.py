# skończone
size = 6

class UnrolledLinkedListElement:
    def __init__(self, nxt=None):
        self.table = [None for _ in range(size)]
        self.filling = 0
        self.next = nxt

    def insert(self, element, idx):
        if self.filling == size:
            raise Exception("Cannot insert the element to the full table.")
        if self.table[idx] is None:
            self.table[idx] = element
        elif self.table[idx] is not None:
            ele, self.table[idx] = self.table[idx], element
            idx += 1
            while ele is not None:
                ele, self.table[idx] = self.table[idx], ele
                idx += 1
        self.filling += 1

    def remove(self, idx):
        if self.table[idx] is None:
            raise Exception("Cannot remove a nonexistent element.")
        elif self.table[idx] is not None:
            if idx < size-1:
                if self.table[idx+1] is None:
                    self.table[idx] = None
                elif self.table[idx+1] is not None:
                    while self.table[idx] is not None:
                        if idx+1 == size:
                            self.table[idx] = None
                        else:
                            self.table[idx] = self.table[idx+1]
                            idx += 1
            else:
                self.table[idx] = None
        self.filling -= 1


class UnrolledLinkedList:
    def __init__(self):
        self.list = UnrolledLinkedListElement()

    def get(self, idx):
        num_of_tables = idx//size
        idx = idx%size
        lis = self.list
        for i in range(num_of_tables):
            lis = lis.next
            if lis is None:
                raise Exception("The given index is too high.")
        if lis.table[idx] is not None:
            return lis.table[idx]
        else:
            raise Exception("The given index is too high or incorrect.")

    def insert(self, element, idx):
        num_of_tables = idx // size
        idx = idx % size
        flag = "OK"
        lis = self.list
        for i in range(num_of_tables):
            if lis.next is None:
                flag = "NOT OK"
                break
            lis = lis.next
        if flag == "NOT OK":
            if lis.filling == size:
                lis.next = UnrolledLinkedListElement()
                lis.next.insert(element, 0)
            else:
                lis.insert(element, lis.filling)
        elif flag == "OK":
            if lis.filling == size:
                if lis.next is not None:
                    lis.next = UnrolledLinkedListElement(lis.next)
                    for i in range(round(size/2)):
                        lis.next.insert(lis.table[round(size/2)], i)
                        lis.remove(round(size/2))
                    if idx >= round(size/2):
                        lis.next.insert(element, idx-round(size / 2))
                    else:
                        lis.insert(element, idx)
                elif lis.next is None:
                    lis.next = UnrolledLinkedListElement()
                    lis.next.insert(element, 0)
            else:
                if idx > lis.filling:
                    lis.insert(element, lis.filling)
                else:
                    lis.insert(element, idx)

    def delete(self, idx):
        num_of_tables = idx // size
        idx = idx % size
        lis = self.list
        for i in range(num_of_tables):
            if lis.next is None:
                raise Exception("Cannot delete a nonexisting element.")
            lis = lis.next
        lis.remove(idx)
        if lis.filling < round(size/2):
            if lis.next is not None:
                lis.insert(lis.next.table[0], lis.filling)
                lis.next.remove(0)
                if lis.next.filling < round(size/2):
                    while lis.next.table[0] is not None:
                        lis.insert(lis.next.table[0], lis.filling)
                        lis.next.remove(0)
                    lis.next = lis.next.next
            elif lis.next is None:
                pass

    def __str__(self):
        string = "[ "
        lis = self.list
        while lis is not None:
            for ele in lis.table:
                string += f"{ele} "
            lis = lis.next
        string += "]"
        return string


def main():
    list = UnrolledLinkedList()

    for i in range(1, 10):
        list.insert(i, i)

    print(list.get(4))

    list.insert(10, 1)
    list.insert(11, 8)

    print(list)

    list.delete(1)
    list.delete(2)

    print(list)


if __name__ == "__main__":
    main()
    