"""Benchmark workload for LeetCode #225 — Implement Stack using Queues (Python; scale lane)."""


class Queue:
    def __init__(self):
        self.data = []
        self.head = 0


def q_new():
    return Queue()


def q_size(q):
    return len(q.data) - q.head


def q_enqueue(q, x):
    q.data.append(x)


def q_dequeue(q):
    v = q.data[q.head]
    q.head += 1
    return v


def q_front(q):
    return q.data[q.head]


def stack_push(q, x):
    q_enqueue(q, x)
    rotations = q_size(q) - 1
    while rotations > 0:
        front = q_dequeue(q)
        q_enqueue(q, front)
        rotations -= 1


def stack_pop(q):
    return q_dequeue(q)


def stack_top(q):
    return q_front(q)


def main():
    passes = 12000
    ops_per_pass = 1500
    cap = 48
    modulus = 1000000007

    state = 12345
    sink = 0
    for _ in range(passes):
        s = q_new()
        for _ in range(ops_per_pass):
            state = (state * 1103515245 + 12345) & 2147483647
            v = (state % 1000) + 1
            sel = state % 4
            size = q_size(s)
            if size == 0:
                stack_push(s, v)
            elif size >= cap:
                if state & 1 == 0:
                    sink = (sink + stack_pop(s)) % modulus
                else:
                    sink = (sink + stack_top(s)) % modulus
            elif sel <= 1:
                stack_push(s, v)
            elif sel == 2:
                sink = (sink + stack_pop(s)) % modulus
            else:
                sink = (sink + stack_top(s)) % modulus
    print(sink)


main()
