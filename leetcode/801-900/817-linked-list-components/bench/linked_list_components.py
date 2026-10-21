# Benchmark for #817: Linked List Components -- mirror of the ★ arm (count
# the ends), with the same workload as linked_list_components.kara.


class ListNode:
    __slots__ = ("val", "next")

    def __init__(self, val, next=None):
        self.val = val
        self.next = next


def num_components(head, nums):
    wanted = set(nums)
    count = 0
    node = head
    while node is not None:
        if node.val in wanted and (node.next is None or node.next.val not in wanted):
            count += 1
        node = node.next
    return count


seed = 817


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, n, rounds = 64, 10000, 8000
    lists, inside, outside = [], [], []
    for _ in range(count):
        order = list(range(n))
        for i in range(n):
            j = i + next_random() % (n - i)
            order[i], order[j] = order[j], order[i]
        head = None
        for k in range(n):
            head = ListNode(order[n - 1 - k], head)
        lists.append(head)
        for i in range(n):
            j = i + next_random() % (n - i)
            order[i], order[j] = order[j], order[i]
        m = 1 + next_random() % (n - 1)
        inside.append(order[:m])
        outside.append(order[m:])
    total = 0
    checksum = 0
    for rnd in range(rounds):
        g = rnd % count
        a = next_random() % len(inside[g])
        b = next_random() % len(outside[g])
        inside[g][a], outside[g][b] = outside[g][b], inside[g][a]
        answer = num_components(lists[g], inside[g])
        total += answer
        checksum = (checksum * 31 + answer) % 1000000007
    print(f"{rounds} rounds of {n} nodes: total {total}, checksum {checksum}")


main()
