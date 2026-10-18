# LeetCode #707: Design Linked List -- singly linked, with a sentinel.
#
# A mirror of design_linked_list.kara (the ★ arm) and its harness.

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


class Node:
    def __init__(self, val, nxt):
        self.val = val
        self.next = nxt


class MyLinkedList:
    def __init__(self):
        self.head = Node(0, None)
        self.size = 0

    def before(self, index):
        at = self.head
        for _ in range(index):
            at = at.next
        return at

    def get(self, index):
        if index < 0 or index >= self.size:
            return -1
        return self.before(index).next.val

    def add_at_head(self, val):
        self.add_at_index(0, val)

    def add_at_tail(self, val):
        self.add_at_index(self.size, val)

    def add_at_index(self, index, val):
        if index < 0 or index > self.size:
            return
        prev = self.before(index)
        prev.next = Node(val, prev.next)
        self.size += 1

    def delete_at_index(self, index):
        if index < 0 or index >= self.size:
            return
        prev = self.before(index)
        prev.next = prev.next.next
        self.size -= 1


def run(ops, indexes, vals):
    lst = MyLinkedList()
    out = []
    for op, index, val in zip(ops, indexes, vals):
        if op == 0:
            out.append(lst.get(index))
            continue
        if op == 1:
            lst.add_at_head(val)
        elif op == 2:
            lst.add_at_tail(val)
        elif op == 3:
            lst.add_at_index(index, val)
        else:
            lst.delete_at_index(index)
        out.append(None)
    contents = []
    while True:
        v = lst.get(len(contents))
        if v < 0:
            break
        contents.append(v)
    return out, contents


def fmt(xs):
    return "[" + ", ".join(str(x) for x in xs) + "]"


def show(ops, indexes, vals):
    calls = []
    for op, index, val in zip(ops, indexes, vals):
        if op == 0:
            calls.append(f"get({index})")
        elif op == 1:
            calls.append(f"addAtHead({val})")
        elif op == 2:
            calls.append(f"addAtTail({val})")
        elif op == 3:
            calls.append(f"addAtIndex({index}, {val})")
        else:
            calls.append(f"deleteAtIndex({index})")
    answers, contents = run(ops, indexes, vals)
    shown = ["null" if a is None else str(a) for a in answers]
    print(f"{', '.join(calls)}: [{', '.join(shown)}], list {fmt(contents)}")


def random_calls(n):
    ops, indexes, vals = [], [], []
    size = 0
    for _ in range(n):
        op = next_random() % 5
        index = next_random() % (size + 3)
        ops.append(op)
        indexes.append(index)
        vals.append(next_random() % 1001)
        if op == 1 or op == 2 or (op == 3 and index <= size):
            size += 1
        elif op == 4 and index < size:
            size -= 1
    return ops, indexes, vals


def checksum(answers, contents):
    total = 0
    for a in answers:
        v = 1 if a is None else a + 2
        total = (total * 31 + v) % 1000000007
    for v in contents:
        total = (total * 31 + v) % 1000000007
    return total


def main():
    global seed
    show([1, 2, 3, 0, 4, 0], [0, 0, 1, 1, 1, 1], [1, 3, 2, 0, 0, 0])
    show([0, 4, 3, 3, 0], [0, 0, 1, 0, 0], [0, 0, 5, 7, 0])
    show([2, 2, 3, 3, 0, 4, 4, 0], [0, 0, 2, 4, 2, 2, 0, 0], [1, 2, 3, 4, 0, 0, 0, 0])
    seed = 707
    for _ in range(2):
        ops, indexes, vals = random_calls(2000)
        answers, contents = run(ops, indexes, vals)
        print(f"2000 calls: {len(contents)} values left, checksum {checksum(answers, contents)}")
    ops = [2] * 1000 + [4] * 500
    indexes = [0] * 1000 + list(range(500))
    vals = list(range(1000)) + [0] * 500
    answers, contents = run(ops, indexes, vals)
    print(f"1000 added, every other deleted: {len(contents)} left, first {contents[0]}, last {contents[-1]}, checksum {checksum(answers, contents)}")
    total = 0
    for _ in range(300):
        n = 1 + next_random() % 100
        ops, indexes, vals = random_calls(n)
        answers, contents = run(ops, indexes, vals)
        total = (total * 31 + checksum(answers, contents)) % 1000000007
    print(f"300 random sequences: checksum {total}")


main()
