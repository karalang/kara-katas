# LeetCode #1188: Design Bounded Blocking Queue -- the bench in Python: the
# ★ arm's two counting semaphores and a lock, a thread per producer and per
# consumer.
import threading
from collections import deque


class BoundedBlockingQueue:
    def __init__(self, capacity):
        self.slots = threading.Semaphore(capacity)
        self.items = threading.Semaphore(0)
        self.lock = threading.Lock()
        self.values = deque()

    def enqueue(self, element):
        self.slots.acquire()
        with self.lock:
            self.values.append(element)
        self.items.release()

    def dequeue(self):
        self.items.acquire()
        with self.lock:
            element = self.values.popleft()
        self.slots.release()
        return element

    def size(self):
        with self.lock:
            return len(self.values)


def run(rnd):
    queue = BoundedBlockingQueue(16)
    total = [0]
    total_lock = threading.Lock()

    def produce(p):
        for k in range(2500):
            queue.enqueue((rnd * 7919 + p * 10007 + k * 31) % 1000)

    def consume():
        s = 0
        for _ in range(2500):
            s += queue.dequeue()
        with total_lock:
            total[0] += s

    threads = [threading.Thread(target=produce, args=(p,)) for p in range(4)]
    threads += [threading.Thread(target=consume) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return total[0] + 1000 * queue.size()


rounds = 100
check = 0
for rnd in range(rounds):
    check = (check * 131 + run(rnd)) % 1000000007
print(f"{rounds} rounds of 4 producers and 4 consumers moving 10000 values through 16 places: checksum {check}")
