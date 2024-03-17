# skończone
class Node:
    def __init__(self, max_children):
        self.keys = (max_children - 1) * [None]
        self.children = max_children * [None]

    def size(self):
        s = 0
        for ele in self.keys:
            if ele is None:
                break
            else:
                s += 1
        return s

    def insert_key(self, key, last_node=None):
        if not (None in self.keys):
            max_size = self.size()
            middle_key = self.keys[max_size // 2]
            new_node = Node(max_size + 1)
            if self.children[0] is None:
                for i in range(max_size):
                    if self.keys[max_size - i - 1] > middle_key:
                        new_node.keys[max_size // 2 - i - 1] = self.keys[max_size - i - 1]
                        self.keys[max_size - i - 1] = None
                    else:
                        break
                if self.keys[max_size // 2] > key and (max_size // 2 - 1 >= 0 and self.keys[max_size // 2 - 1] < key):
                    middle_key = key
                    new_node.insert_key(self.keys[max_size // 2])
                    self.keys[max_size // 2] = None
                elif self.keys[max_size // 2] < key:
                    new_node.insert_key(key)
                    self.keys[max_size // 2] = None
                else:
                    middle_key = self.keys[max_size // 2 - 1]
                    new_node.insert_key(self.keys[max_size // 2])
                    self.keys[max_size // 2] = None
                    self.keys[max_size // 2 - 1] = None
                    self.insert_key(key)
            else:
                for i in range(max_size):
                    if self.keys[max_size - i - 1] > middle_key:
                        new_node.keys[max_size // 2 - i - 1] = self.keys[max_size - i - 1]
                        self.keys[max_size - i - 1] = None
                        new_node.children[max_size // 2 - i] = self.children[max_size - i]
                        self.children[max_size - i] = None
                    else:
                        break
                if self.keys[max_size // 2] > key and (max_size // 2 - 1 >= 0 and self.keys[max_size // 2 - 1] < key):
                    new_node.children[0] = last_node
                    middle_key = key
                    new_node.insert_key(self.keys[max_size // 2], self.children[max_size // 2 + 1])
                    self.keys[max_size // 2] = None
                    self.children[max_size // 2 + 1] = None
                elif self.keys[max_size // 2] < key:
                    new_node.children[0] = self.children[max_size // 2 + 1]
                    new_node.insert_key(key, last_node)
                    self.keys[max_size // 2] = None
                    self.children[max_size // 2 + 1] = None
                else:
                    new_node.children[0] = self.children[max_size // 2]
                    middle_key = self.keys[max_size // 2 - 1]
                    new_node.insert_key(self.keys[max_size // 2], self.children[max_size // 2 + 1])
                    self.keys[max_size // 2] = None
                    self.children[max_size // 2 + 1] = None
                    self.keys[max_size // 2 - 1] = None
                    self.children[max_size // 2] = None
                    self.insert_key(key, last_node)
            return middle_key, new_node
        else:
            self.keys[self.size()] = key
            if self.children[0] is None:
                for i in range(self.size()):
                    if self.size() - i - 1 > 0 and self.keys[self.size() - 2 - i] > self.keys[self.size() - 1 - i]:
                        self.keys[self.size() - 2 - i], self.keys[self.size() - 1 - i] = self.keys[self.size() - 1 - i], self.keys[self.size() - 2 - i]
                    else:
                        break
            else:
                self.children[self.size()] = last_node
                for i in range(self.size()):
                    if self.size() - i - 1 > 0 and self.keys[self.size() - 2 - i] > self.keys[self.size() - 1 - i]:
                        self.keys[self.size() - 2 - i], self.keys[self.size() - 1 - i] = self.keys[self.size() - 1 - i], self.keys[self.size() - 2 - i]
                        self.children[self.size() - 1 - i], self.children[self.size() - i] = self.children[self.size() - i], self.children[self.size() - 1 - i]
                    else:
                        break
            return None


class BTree:
    def __init__(self, max_children):
        self.max_children = max_children
        self.root = Node(max_children)

    def insert(self, key, node=None):
        if node is None:
            node = self.root
        flag = 'not_inserted'
        for i in range(self.max_children - 1):
            if node.keys[i] is None or node.keys[i] > key:
                flag = 'is_inserted'
                if node.children[0] is None:
                    info = node.insert_key(key)
                    if node == self.root and info is not None:
                        new_node = Node(self.max_children)
                        new_node.keys[0] = info[0]
                        new_node.children[0] = self.root
                        new_node.children[1] = info[1]
                        self.root = new_node
                        return None
                    else:
                        return info
                else:
                    info = self.insert(key, node.children[i])
                break
        if flag != 'is_inserted':
            if node.children[self.max_children - 1] is None:
                info = node.insert_key(key)
                if node == self.root and info is not None:
                    new_node = Node(self.max_children)
                    new_node.keys[0] = info[0]
                    new_node.children[0] = self.root
                    new_node.children[1] = info[1]
                    self.root = new_node
                    return None
                else:
                    return info
            else:
                info = self.insert(key, node.children[self.max_children - 1])
        if info is not None:
            info_new = node.insert_key(info[0], info[1])
            if node == self.root and info_new is not None:
                new_node = Node(self.max_children)
                new_node.keys[0] = info_new[0]
                new_node.children[0] = self.root
                new_node.children[1] = info_new[1]
                self.root = new_node
                return None
            else:
                return info_new
        else:
            info_new = None
        return info_new

    def print_tree(self):
        print("==============")
        self._print_tree(self.root, 0)
        print("==============")

    def _print_tree(self, node, lvl):
        if node is not None:
            for i in range(node.size() + 1):
                self._print_tree(node.children[i], lvl + 1)
                if i < node.size():
                    print(lvl * '  ', node.keys[i])


def main():
    btree1 = BTree(4)
    for key in [5, 17, 2, 14, 7, 4, 12, 1, 16, 8, 11, 9, 6, 13, 0, 3, 18, 15, 10, 19]:
        btree1.insert(key)
    btree1.print_tree()

    btree2 = BTree(4)
    for key in range(20):
        btree2.insert(key)
    btree2.print_tree()

    for key in range(20, 200):
        btree2.insert(key)
    btree2.print_tree()

    btree3 = BTree(6)
    for key in range(200):
        btree3.insert(key)
    btree3.print_tree()


if __name__ == "__main__":
    main()
