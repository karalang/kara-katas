"""LeetCode 225 — Implement Stack using Queues (Python mirror / oracle).

Single index-pool FIFO queue (list + head cursor); costly push rotates the new
element to the front so pop/top read LIFO order. Mirrors the Kara version.
"""


class Queue:
    def __init__(self):
        self.data = []
        self.head = 0

    def size(self):
        return len(self.data) - self.head

    def empty(self):
        return self.head >= len(self.data)

    def enqueue(self, x):
        self.data.append(x)

    def dequeue(self):
        v = self.data[self.head]
        self.head += 1
        return v

    def front(self):
        return self.data[self.head]


def stack_push(q, x):
    q.enqueue(x)
    rotations = q.size() - 1
    while rotations > 0:
        q.enqueue(q.dequeue())
        rotations -= 1


def stack_pop(q):
    return q.dequeue()


def stack_top(q):
    return q.front()


def stack_empty(q):
    return q.empty()


def show_bool(b):
    print("true" if b else "false")


def main():
    s = Queue()

    stack_push(s, 1)
    stack_push(s, 2)
    print(stack_top(s))
    print(stack_pop(s))
    show_bool(stack_empty(s))

    stack_push(s, 3)
    stack_push(s, 4)
    print(stack_top(s))
    print(stack_pop(s))
    print(stack_pop(s))
    print(stack_pop(s))
    show_bool(stack_empty(s))

    stack_push(s, 5)
    print(stack_top(s))
    show_bool(stack_empty(s))


main()
