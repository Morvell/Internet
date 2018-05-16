from collections import OrderedDict


class PriorityQueue:

    def __init__(self):
        self.array = []

    def enqueue(self, key, value):
        for i in range(len(self.array)):
            if self.array[i][1] > value:
                self.array.insert(i, (key, value))
                return
        self.array.append((key, value))

    def dequeue(self):
        return self.array.pop()

    @property
    def empty(self):
        return len(self.array) == 0
