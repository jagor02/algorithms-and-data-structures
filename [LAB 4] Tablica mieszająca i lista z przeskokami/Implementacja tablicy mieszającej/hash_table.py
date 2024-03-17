# skończone
class HashTableElement:
    def __init__(self, data, key):
        self.data = data
        self.key = key


class HashTable:
    def __init__(self, size, c1=1, c2=0):
        self.table = [None for _ in range(size)]
        self.c1 = c1
        self.c2 = c2

    def hashing(self, key):
        if isinstance(key, str):
            s = 0
            for letter in key:
                s += ord(letter)
            key = s
        idx = key % len(self.table)
        return idx

    def solve_collision(self, element=None, key=None, status=None):
        if status not in ["insert", "search", "remove"]:
            raise Exception("Nieobsługiwana komenda.")
        if (isinstance(element, HashTableElement) and key is None) or ((isinstance(key, int) or isinstance(key, str))
                                                                       and element is None):
            if isinstance(element, HashTableElement) and key is None:
                idx = self.hashing(element.key)
            else:
                idx = self.hashing(key)
            for i in range(1, len(self.table)):
                new_idx = self.hashing(idx + self.c1 * i + self.c2 * i ** 2)
                if (self.table[new_idx] is None or self.table[new_idx].data is None) and status == "insert":
                    self.table[new_idx] = element
                    return "Success"
                elif isinstance(self.table[new_idx], HashTableElement):
                    if status == "search" and self.table[new_idx].key == key:
                        return self.table[new_idx].data
                    elif status == "insert" and self.table[new_idx].key == element.key:
                        self.table[new_idx] = element
                        return "Success"
                    elif status == "remove" and self.table[new_idx].key == key and self.table[new_idx].data is not None:
                        self.table[new_idx].data = None
                        return "Success"
            return "Fail"
        raise Exception("Podano element oraz key.")

    def search(self, key):
        idx = self.hashing(key)
        if self.table[idx] is None:
            return None
        elif isinstance(self.table[idx], HashTableElement) and self.table[idx].key == key:
            return self.table[idx].data
        flag = self.solve_collision(key=key, status="search")
        if flag == "Fail":
            return None
        return flag

    def insert(self, element):
        idx = self.hashing(element.key)
        if self.table[idx] is None or self.table[idx].data is None:
            self.table[idx] = element
        elif isinstance(self.table[idx], HashTableElement) and self.table[idx].key == element.key:
            self.table[idx] = element
        else:
            flag = self.solve_collision(element=element, status="insert")
            if flag == "Fail":
                raise Exception("Brak miejsca")

    def remove(self, key):
        idx = self.hashing(key)
        if isinstance(self.table[idx], HashTableElement) and self.table[idx].key == key and self.table[idx].data is not None:
            self.table[idx].data = None
        else:
            flag = self.solve_collision(key=key, status="remove")
            if flag == "Fail":
                raise Exception("Brak danej")

    def __str__(self):
        string = '{ '
        for i in range(len(self.table) - 1):
            if self.table[i] is None or self.table[i].data is None:
                string += "None, "
            else:
                string += f"{self.table[i].key}:{self.table[i].data}, "
        if self.table[len(self.table) - 1] is None or self.table[len(self.table) - 1].data is None:
            string += "None "
        else:
            string += f"{self.table[len(self.table) - 1].key}:{self.table[len(self.table) - 1].data} "
        string += '}'
        return string


def test_function_one(size, c1, c2):
    hash_table = HashTable(size, c1, c2)

    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']
    for i in range(1, 16):
        letter = letters[i - 1]
        if i == 6:
            i = 18
        elif i == 7:
            i = 31
        try:
            hash_table.insert(HashTableElement(letter, i))
        except Exception:
            print("Brak miejsca")

    print(hash_table)

    print(hash_table.search(5))

    print(hash_table.search(14))

    try:
        hash_table.insert(HashTableElement('Z', 5))
    except Exception:
        print("Brak miejsca")

    print(hash_table.search(5))

    try:
        hash_table.remove(5)
    except Exception:
        print("Brak danej")

    print(hash_table)

    print(hash_table.search(31))

    try:
        hash_table.insert(HashTableElement('W', "test"))
    except Exception:
        print("Brak miejsca")

    print(hash_table)


def test_function_two(size, c1, c2):
    hash_table = HashTable(size, c1, c2)

    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']
    for i in range(1, 16):
        letter = letters[i - 1]
        try:
            hash_table.insert(HashTableElement(letter, i * 13))
        except Exception:
            print("Brak miejsca")

    print(hash_table)


def main():
    test_function_one(size=13, c1=1, c2=0)
    test_function_two(size=13, c1=1, c2=0)
    test_function_two(size=13, c1=0, c2=1)
    test_function_one(size=13, c1=0, c2=1)


if __name__ == "__main__":
    main()
