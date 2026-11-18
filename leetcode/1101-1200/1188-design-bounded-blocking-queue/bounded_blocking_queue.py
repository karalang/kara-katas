# LeetCode #1188: Design Bounded Blocking Queue -- the ★ arm in Python: two
# counting semaphores and a lock, a thread per producer and per consumer.
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


seed = 1188


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def run(capacity, producers, consumers, values, dequeues):
    queue = BoundedBlockingQueue(capacity)
    out = []
    out_lock = threading.Lock()

    def produce(mine):
        for v in mine:
            queue.enqueue(v)

    def consume(calls):
        for _ in range(calls):
            v = queue.dequeue()
            with out_lock:
                out.append(v)

    threads = []
    for p in range(producers):
        mine = [values[i] for i in range(len(values)) if i % producers == p]
        threads.append(threading.Thread(target=produce, args=(mine,)))
    for c in range(consumers):
        calls = sum(1 for i in range(dequeues) if i % consumers == c)
        threads.append(threading.Thread(target=consume, args=(calls,)))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    size = queue.size()
    rest = [queue.dequeue() for _ in range(size)]
    return out, size, rest


def accounted(values, got, rest):
    return sorted(got + rest) == sorted(values)


def show(capacity, producers, consumers, values, dequeues):
    got, size, rest = run(capacity, producers, consumers, values, dequeues)
    if producers == 1 and consumers == 1:
        return "[" + ",".join(str(v) for v in got) + f",{size}]"
    ok = "true" if accounted(values, got, rest) else "false"
    return f"{len(got)} dequeued, size {size}, every value accounted for: {ok}"


print(show(2, 1, 1, [1, 0, 2, 3, 4], 3))
print(show(3, 3, 4, [1, 0, 2, 3], 3))
print(show(1, 1, 1, [5, 6, 7, 8], 4))
print(show(30, 1, 1, [i % 21 for i in range(40)], 10))
whole = in_order = left = 0
for _ in range(2000):
    capacity = next_random() % 30 + 1
    producers = next_random() % 8 + 1
    consumers = next_random() % 8 + 1
    n = next_random() % 40 + 1
    values = [next_random() % 21 for _ in range(n)]
    fewest = n - capacity if n > capacity else 0
    dequeues = fewest + next_random() % (n - fewest + 1)
    got, size, rest = run(capacity, producers, consumers, values, dequeues)
    left += size
    if accounted(values, got, rest):
        whole += 1
    if producers == 1 and consumers == 1 and got == values[:dequeues]:
        in_order += 1
print(f"2000 random runs: {left} left over, {whole} with every value accounted for, {in_order} in order with one of each")
