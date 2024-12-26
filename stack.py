class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)
        
    def pop(self, index=None):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        
        if index is None:
            return self.items.pop()
        else:
            if index < 0 or index >= len(self.items):
                raise IndexError("index out of range")
            return self.items.pop(index)

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        else:
            raise IndexError("peek from empty stack")

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)
