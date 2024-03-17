# skończone
class LinkedListElement:
    def __init__(self, data, nxt=None):
        if isinstance(nxt, LinkedListElement) or nxt is None:
            self.data = data
            self.next = nxt
        else:
            raise Exception("Argument 'nxt' is not LinkedListElement instance (and doesn't point at None).")

class LinkedList:
    def __init__(self):
        self.head = None
        
    def destroy(self):
        if self.head is not None:
            self.head = None
        
    def add(self, data):
        if self.head is None:
            element = LinkedListElement(data)
        else:
            element = LinkedListElement(data, self.head)
        self.head = element
    
    def append(self, data):
        if self.head is None:
            self.head = LinkedListElement(data)
        else:
            element = self.head
            while element.next is not None:
                element = element.next
            element.next = LinkedListElement(data)
        
    def remove(self):
        if self.head is None:
            pass
        else:
            self.head = (self.head).next
            
    def remove_end(self):
        if self.head is None:
            pass
        else:
            element = self.head
            while (element.next).next is not None:
                element = element.next
            element.next = None
            
    def is_empty(self):
        return True if self.head is None else False
        
    def length(self):
        l = 0
        if self.head is not None:
            l = 1
            element = self.head
            while element.next is not None:
                l += 1
                element = element.next
        return l
        
    def get(self):
        if self.head is None:
            raise Exception("Linked list has no elements right now.")
        else:
            return (self.head).data
            
    def __str__(self):
        text = ''
        if self.head is not None:
            element = self.head
            for _ in range(self.length()):
                text += f'-> {element.data}\n'
                element = element.next
        return text
        
def main():
    lst = [('AGH', 'Kraków', 1919),
           ('UJ', 'Kraków', 1364),
           ('PW', 'Warszawa', 1915),
           ('UW', 'Warszawa', 1915),
           ('UP', 'Poznań', 1919),
           ('PG', 'Gdańsk', 1945)]
            
    uczelnie = LinkedList()
    
    uczelnie.append(lst[0])
    uczelnie.append(lst[1])
    uczelnie.append(lst[2])
    
    uczelnie.add(lst[3])
    uczelnie.add(lst[4])
    uczelnie.add(lst[5])
    
    print(uczelnie)
    
    print(uczelnie.length())
    
    uczelnie.remove()
    
    print(uczelnie.get())
    
    uczelnie.remove_end()
    
    print(uczelnie)
    
    uczelnie.destroy()
    print(uczelnie.is_empty())
    
    uczelnie.remove()
    
    uczelnie.remove_end()
    
if __name__ == "__main__":
    main()
