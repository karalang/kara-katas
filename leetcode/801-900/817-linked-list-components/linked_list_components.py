# LeetCode 817 — Linked List Components, count the ends (mirror of the ★ arm).


class ListNode:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next


def num_components(head, nums):
    wanted = set(nums)
    count = 0
    cur = head
    while cur is not None:
        if cur.val in wanted and (cur.next is None or cur.next.val not in wanted):
            count += 1
        cur = cur.next
    return count


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def from_values(values):
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head


def show(values, nums):
    print(f"head = {values}, nums = {nums} -> {num_components(from_values(values), nums)}")


def shuffled(n):
    values = list(range(n))
    for i in range(n):
        j = i + next_random() % (n - i)
        values[i], values[j] = values[j], values[i]
    return values


def main():
    global seed
    show([0, 1, 2, 3], [0, 1, 3])
    show([0, 1, 2, 3, 4], [0, 3, 1, 4])
    show([0], [0])
    show([2, 0, 1], [1, 2])
    show([3, 1, 4, 0, 2], [2, 0, 3])
    show([0, 1, 2, 3, 4, 5], [5, 3, 1])
    show([0, 1, 2, 3, 4, 5], [4, 2, 0, 5, 1, 3])
    seed = 817
    values = shuffled(10000)
    half = shuffled(10000)[0:5000]
    print(f"10000 nodes, a random half -> {num_components(from_values(values), half)}")
    alternate = [values[2 * k] for k in range(5000)]
    print(f"10000 nodes, every other one -> {num_components(from_values(values), alternate)}")
    total = 0
    check = 0
    for _ in range(300):
        n = 1 + next_random() % 30
        values = shuffled(n)
        m = 1 + next_random() % n
        nums = shuffled(n)[0:m]
        answer = num_components(from_values(values), nums)
        total += answer
        check = (check * 131 + answer) % 1000000007
    print(f"300 random rounds of 1 to 30 nodes: total {total}, checksum {check}")


main()
