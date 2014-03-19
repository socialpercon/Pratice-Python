
-- iterablequeue
   * Queue.Queue는 iterable하지 않기 때문에 따로 재정의 해줘야 한다.

-- iterable_queue_simple
   * get 같은 걸 재정의 안해 줄 때는 이 코드가 간결하다.
   * 하지만 재정의 해줘야할 경우 iterable_queue 코드를 활용해야 한다.

-- iterable_queue_last
   * queue.get을 할 경우 입력이 들어 올때 까지 block 상태가 된다.
   * get을 재정의 하여 block 상태를 꺼줘야 한다.
```
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
```
