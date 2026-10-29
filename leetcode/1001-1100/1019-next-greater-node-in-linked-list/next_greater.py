# LeetCode #1019: Next Greater Node In Linked List -- a stack of waiting
# nodes
# Mirrors next_greater.kara; its output is byte-identical.


class ListNode:
    def __init__(self, val, nxt=None):
        self.val = val
        self.next = nxt


def next_larger_nodes(head):
    values = []
    answer = []
    waiting = []
    cur = head
    while cur is not None:
        v = cur.val
        while waiting and values[waiting[-1]] < v:
            answer[waiting.pop()] = v
        waiting.append(len(values))
        values.append(v)
        answer.append(0)
        cur = cur.next
    return answer


seed = 1019


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def from_values(values):
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head


def shown(xs):
    return "[" + ", ".join(str(x) for x in xs) + "]"


def main():
    examples = [
        [2, 1, 5],
        [2, 7, 4, 3, 5],
        [1],
        [5, 4, 3, 2, 1],
        [1, 2, 3, 4, 5],
        [3, 3, 3],
        [1, 7, 5, 1, 9, 2, 5, 1],
        [9, 1, 1, 1, 9, 10],
    ]
    for values in examples:
        print(f"{shown(values)} -> {shown(next_larger_nodes(from_values(values)))}")
    groups = [(1000, 10, 10), (300, 100, 1000), (30, 1000, 1000000000), (30, 1000, 3), (3, 3000, 1000000000)]
    for count, length, most in groups:
        total = zeros = check = 0
        for _ in range(count):
            values = []
            for _ in range(length):
                hi = next_random()
                values.append((hi * 32768 + next_random()) % most + 1)
            for a in next_larger_nodes(from_values(values)):
                total += a
                if a == 0:
                    zeros += 1
                check = (check * 31 + a) % 1000000007
        print(f"{count} random lists of {length} values up to {most}: answers sum to {total}, {zeros} are 0, checksum {check}")
    down = next_larger_nodes(from_values([3000 - i for i in range(3000)]))
    up = next_larger_nodes(from_values([i + 1 for i in range(3000)]))
    print(f"falling 3000: answers sum to {sum(down)}; rising 3000: answers sum to {sum(up)}")


main()
