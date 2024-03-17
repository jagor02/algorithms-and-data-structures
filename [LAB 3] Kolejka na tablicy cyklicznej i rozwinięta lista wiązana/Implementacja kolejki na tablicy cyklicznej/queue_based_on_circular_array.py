# skończone
class Queue:
    def __init__(self):
        self.size = 5
        self.table = [None for _ in range(self.size)]
        self.save_idx = 0
        self.read_idx = 0
    
    def is_empty(self):
        return True if self.save_idx == self.read_idx else False
        
    def peek(self):
        return None if self.is_empty() else self.table[self.read_idx]
        
    def dequeue(self):
        if self.is_empty():
            return None
        else:
            ele = self.table[self.read_idx]
            self.table[self.read_idx] = None
            if self.read_idx < self.size-1:
                self.read_idx += 1
            elif self.read_idx == self.size-1:
                self.read_idx = 0
            return ele
    
    def enqueue(self, data):
        self.table[self.save_idx] = data
        if self.save_idx < self.size-1:
            self.save_idx += 1
        elif self.save_idx == self.size-1:
            self.save_idx = 0
        if self.save_idx == self.read_idx:
            self.realloc()
            self.read_idx += self.size
            self.size *= 2
    
    def realloc(self):
        table = [None for _ in range(2*self.size)]
        for i in range(2*self.size):
            if i < self.save_idx:
                table[i] = self.table[i]
            elif i >= self.save_idx+self.size:
                table[i] = self.table[i-self.size]
        self.table = table
    
    def __str__(self):
        string = '[ '
        idx = self.read_idx
        while idx != self.save_idx:
            string += f"{self.table[idx]} "
            if idx < self.size-1:
                idx += 1
            elif idx == self.size-1:
                idx = 0
        string += ']'
        return string
        
    def print_table(self):
        return f"{self.table}"
        

def main():
    queue = Queue()
    
    queue.enqueue(1)
    queue.enqueue(2)
    queue.enqueue(3)
    queue.enqueue(4)
    
    print(queue.dequeue())
    
    print(queue.peek())
    
    print(queue)

    queue.enqueue(5)
    queue.enqueue(6)
    queue.enqueue(7)
    queue.enqueue(8)
    
    print(queue.print_table())
    
    while not queue.is_empty():
        print(queue.dequeue())
        
    print(queue)
    

if __name__=="__main__":
    main()
