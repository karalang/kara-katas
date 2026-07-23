"""LeetCode 232 — Implement Queue using Stacks (Python mirror / oracle).

Two stacks (inbox/outbox); pour inbox into outbox only when the outbox is empty,
which reverses order so the front sits on top. Amortized O(1). Mirrors the Kara
version.
"""


class MyQueue:
    def __init__(self):
        self.inbox = []
        self.outbox = []


def q_push(q, x):
    q.inbox.append(x)


def refill(q):
    if len(q.outbox) == 0:
        while len(q.inbox) > 0:
            q.outbox.append(q.inbox.pop())


def q_pop(q):
    refill(q)
    return q.outbox.pop() if q.outbox else -1


def q_peek(q):
    refill(q)
    return q.outbox[-1]


def q_empty(q):
    return len(q.inbox) == 0 and len(q.outbox) == 0


def show_bool(b):
    print("true" if b else "false")


def main():
    q = MyQueue()

    q_push(q, 1)
    q_push(q, 2)
    q_push(q, 3)
    print(q_peek(q))
    print(q_pop(q))
    print(q_pop(q))
    show_bool(q_empty(q))

    q_push(q, 4)
    print(q_pop(q))
    print(q_pop(q))
    show_bool(q_empty(q))

    q_push(q, 5)
    print(q_peek(q))
    show_bool(q_empty(q))


main()
