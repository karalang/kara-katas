# LeetCode #1019: Next Greater Node In Linked List -- bench
# Mirrors next_greater.kara; see ../README.md § Benchmarks.


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


def main():
    count = 500
    rounds = 10
    lists = []
    nodes = 0
    for _ in range(count):
        length = next_random() % 10000 + 1
        values = []
        for _ in range(length):
            hi = next_random()
            values.append((hi * 32768 + next_random()) % 1000000000 + 1)
        nodes += length
        head = None
        for v in reversed(values):
            head = ListNode(v, head)
        lists.append(head)
    total = 0
    check = 0
    for _ in range(rounds):
        for head in lists:
            for a in next_larger_nodes(head):
                total = (total + a) % 1000000007
                check = (check * 31 + a) % 1000000007
    print(f"{count} lists, {nodes} nodes, {rounds} rounds: answer sum {total}, checksum {check}")


main()
