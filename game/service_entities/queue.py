class Queue:
    def __init__(self):
        self._queue = []

    def enqueue(self, value):
        self._queue.append(value)

    def dequeue(self):
        if len(self._queue):
            result = self._queue.pop(0)
            return result
        raise ValueError("Queue is empty")

    @property
    def head(self):
        return self._queue[0] if len(self._queue) else None

    @property
    def tail(self):
        return self._queue[-1] if len(self._queue) else None

    def __iter__(self):
        return iter(self._queue)

    def __len__(self):
        return len(self._queue)
