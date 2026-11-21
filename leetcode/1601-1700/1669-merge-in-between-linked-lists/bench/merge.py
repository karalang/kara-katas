# LeetCode #1669: Merge In Between Linked Lists -- the bench's Python
# mirror: the ★ arm on one list of 100000 nodes, 10000 times cut at a
# random place, 1 to 8 nodes taken out and a new list of 1 to 8 put in,
# every cut and value drawn first.


class ListNode:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next


def merge_in_between(list1, a, b, list2):
    before = list1
    for _ in range(1, a):
        before = before.next
    after = before.next
    for _ in range(a, b + 1):
        after = after.next
    last = list2
    while last.next is not None:
        last = last.next
    before.next = list2
    last.next = after
    return list1


# ---- the harness ----------------------------------------------------------

seed = 1669


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def build(values):
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head


start = 100000
rounds = 10000
values = [(next_random() * 32768 + next_random()) % 1000001 for _ in range(start)]
length = start
cuts = []
for _ in range(rounds):
    m = next_random() % 8 + 1
    a = (next_random() * 32768 + next_random()) % (length - 2) + 1
    b = a + next_random() % min(8, length - 1 - a)
    list2 = [(next_random() * 32768 + next_random()) % 1000001 for _ in range(m)]
    length += m - (b - a + 1)
    cuts.append((a, b, list2))
lst = build(values)
for a, b, list2 in cuts:
    lst = merge_in_between(lst, a, b, build(list2))
nodes = 0
check = 0
cur = lst
while cur is not None:
    nodes += 1
    check = (check * 31 + cur.val + 1) % 1000000007
    cur = cur.next
print(f"{start} nodes, {rounds} merges: {nodes} nodes, checksum {check}")
