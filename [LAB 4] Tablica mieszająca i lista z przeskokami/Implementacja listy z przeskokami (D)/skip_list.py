# skończone
from random import random


class SkipListElement:
    def __init__(self, key, value, height):
        self.key = key
        self.value = value
        self.height = height
        self.next_table = [None for _ in range(self.height)]


class SkipList:
    def __init__(self, max_height):
        self.max_height = max_height
        self.head = SkipListElement("empty", "empty", max_height)

    def search(self, key):
        search_element = self.head
        for lvl in range(self.max_height-1, -1, -1):
            while search_element.next_table[lvl] is not None and search_element.next_table[lvl].key <= key:
                search_element = search_element.next_table[lvl]
            if search_element.key == key:
                return search_element.value
        return None

    def insert(self, key, value):
        if self.search(key) is not None:
            self.remove(key)
        element = SkipListElement(key, value, random_level(0.5, self.max_height))
        prev_table = [None for _ in range(element.height)]
        search_element = self.head
        for lvl in range(element.height-1, -1, -1):
            while search_element.next_table[lvl] is not None and (search_element.next_table[lvl]).key < key:
                search_element = search_element.next_table[lvl]
            prev_table[lvl] = search_element
        for lvl in range(element.height-1, -1, -1):
            element.next_table[lvl] = prev_table[lvl].next_table[lvl]
            prev_table[lvl].next_table[lvl] = element

    def remove(self, key):
        prev_table = [None for _ in range(self.max_height)]
        search_element = self.head
        for lvl in range(self.max_height-1, -1, -1):
            while search_element.next_table[lvl] is not None and (search_element.next_table[lvl]).key < key:
                search_element = search_element.next_table[lvl]
            prev_table[lvl] = search_element
        if search_element.next_table[0].key == key:
            for lvl in range(self.max_height-1, -1, -1):
                if prev_table[lvl].next_table[lvl] == search_element.next_table[0]:
                    prev_table[lvl].next_table[lvl] = search_element.next_table[0].next_table[lvl]
        else:
            raise Exception("There is no element with given key already.")

    def __str__(self):
        string = ""
        element = self.head.next_table[0]
        while element is not None:
            string += "(" + str(element.key) + ":" + str(element.value) + ")"
            element = element.next_table[0]
        return string

    def displaylist_(self):
        node = self.head.next_table[0]
        keys = []
        while node is not None:
            keys.append(node.key)
            node = node.next_table[0]

        for lvl in range(self.max_height - 1, -1, -1):
            print("{}: ".format(lvl), end=" ")
            node = self.head.next_table[lvl]
            idx = 0
            while node is not None:
                while node.key > keys[idx]:
                    print("  ", end=" ")
                    idx += 1
                idx += 1
                print("{:2d}".format(node.key), end=" ")
                node = node.next_table[lvl]
            print("")


def random_level(p, maxlevel):
    lvl = 1
    while random() < p and lvl < maxlevel:
        lvl += 1
    return lvl


def main():
    height = 6
    
    skiplist1 = SkipList(height)
    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']
    for i in range(15):
        skiplist1.insert(i+1, alphabet[i])
    print(skiplist1)
    print(skiplist1.search(2))
    skiplist1.insert(2, 'Z')
    print(skiplist1.search(2))
    for i in range(5, 8):
        skiplist1.remove(i)
    print(skiplist1)
    skiplist1.insert(6, 'W')
    print(skiplist1)

    skiplist2 = SkipList(height)
    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']
    for i in range(15, 0, -1):
        skiplist2.insert(i, alphabet[i-1])
    print(skiplist2)
    print(skiplist2.search(2))
    skiplist2.insert(2, 'Z')
    print(skiplist2.search(2))
    for i in range(5, 8):
        skiplist2.remove(i)
    print(skiplist2)
    skiplist2.insert(6, 'W')
    print(skiplist2)


if __name__ == "__main__":
    main()
