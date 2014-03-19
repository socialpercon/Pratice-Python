from Queue import Queue

class IterableQueue(Queue): 

    _sentinel = object()

    def __iter__(self):
        return self

    def close(self):
        self.put(self._sentinel)

    def next(self):
        item = self.get()
        if item is self._sentinel:
            raise StopIteration
        else:
            return item
