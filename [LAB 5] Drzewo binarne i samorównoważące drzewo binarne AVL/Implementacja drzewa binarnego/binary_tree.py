# skończone

class BST:
    def __init__(self, root=None):
        self.root = root

    def search(self, key):
        return self.__search(self.root, key)

    def __search(self, node, key):
        if node is None:
            return None
        else:
            if key < node.key:
                return self.__search(node.left, key)
            elif key > node.key:
                return self.__search(node.right, key)
            else:
                return node.value

    def insert(self, key, data):
        if self.root is not None:
            self.__insert(self.root, key, data)
        else:
            self.root = Node(key, data)

    def __insert(self, node, key, data):
        if node is None:
            node = Node(key, data)
            return node
        else:
            if key < node.key:
                node.left = self.__insert(node.left, key, data)
                return node
            elif key > node.key:
                node.right = self.__insert(node.right, key, data)
                return node
            else:
                node.value = data
                return node

    def delete(self, key):
        self.__delete(self.root, key)

    def __delete(self, node, key):
        if node is None:
            raise Exception("Element with given key doesn't exist.")
        else:
            if key < node.key:
                node.left = self.__delete(node.left, key)
                return node
            elif key > node.key:
                node.right = self.__delete(node.right, key)
                return node
            else:
                if node.left is None and node.right is None:
                    return None
                elif node.left is not None and node.right is not None:
                    search_node = node.right
                    if search_node.left is not None:
                        while search_node.left.left is not None:
                            search_node = search_node.left
                        node.key = search_node.left.key
                        node.value = search_node.left.value
                        search_node.left = None
                    else:
                        search_node.left = node.left
                        node = search_node
                    return node
                else:
                    if node.left is None:
                        return node.right
                    else:
                        return node.left

    def print(self):
        string = ""
        string += self.__print(self.root)
        print(string)

    def __print(self, node):
        string = ""
        if node.left is not None:
            string += self.__print(node.left)
        string += str(node.key) + " " + str(node.value) + ","
        if node.right is not None:
            string += self.__print(node.right)
        return string

    def height(self, node=None):
        if node is not None:
            h = self.__height(node)
        else:
            h = self.__height(self.root)
        return h

    def __height(self, node):
        left = 0
        right = 0
        if node.left is not None:
            left += 1
            left += self.__height(node.left)
        if node.right is not None:
            right += 1
            right += self.__height(node.right)
        if left > right:
            return left
        else:
            return right

    def print_tree(self):
        print("==============")
        self.__print_tree(self.root, 0)
        print("==============")

    def __print_tree(self, node, lvl):
        if node is not None:
            self.__print_tree(node.right, lvl + 5)

            print()
            print(lvl * " ", node.key, node.value)

            self.__print_tree(node.left, lvl + 5)


class Node:
    def __init__(self, key, value, left=None, right=None):
        self.key = key
        self.value = value
        self.left = left
        self.right = right


def main():
    tree_bst = BST()
    for key, value in {50:'A', 15:'B', 62:'C', 5:'D', 20:'E', 58:'F', 91:'G', 3:'H', 8:'I', 37:'J', 60:'K', 24:'L'}.items():
        tree_bst.insert(key, value)
    tree_bst.print_tree()
    tree_bst.print()
    print(tree_bst.search(24))
    tree_bst.insert(20, 'AA')
    tree_bst.insert(6, 'M')
    tree_bst.delete(62)
    tree_bst.insert(59, 'N')
    tree_bst.insert(100, 'P')
    tree_bst.delete(8)
    tree_bst.delete(15)
    tree_bst.insert(55, 'R')
    tree_bst.delete(50)
    tree_bst.delete(5)
    tree_bst.delete(24)
    print(tree_bst.height())
    tree_bst.print()
    tree_bst.print_tree()


if __name__ == "__main__":
    main()
    