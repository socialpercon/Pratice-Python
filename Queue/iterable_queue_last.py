from Queue import Queue, Empty

class IterableQueue(Queue):

    def __iter__(self):
        return self

    def next(self):
        try:
            item = self.get(block=False)
            return item
        except Empty:
            raise StopIteration
