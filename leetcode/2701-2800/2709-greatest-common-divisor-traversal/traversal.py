# LeetCode #2709: Greatest Common Divisor Traversal -- the Python mirror
# of the star arm (traversal.kara): each index joined, in a union-find,
# to the first index that shares each of its prime factors, read off a
# smallest-prime-factor sieve; the answer is whether one set holds all.


def find(parent, a):
    while parent[a] != a:
        parent[a] = parent[parent[a]]
        a = parent[a]
    return a


def can_traverse_all_pairs(nums):
    n = len(nums)
    if n == 1:
        return True
    top = max(nums)
    spf = list(range(top + 1))
    p = 2
    while p * p <= top:
        if spf[p] == p:
            for m in range(p * p, top + 1, p):
                if spf[m] == m:
                    spf[m] = p
        p += 1
    parent = list(range(n))
    first = [-1] * (top + 1)
    sets = n
    for i, v in enumerate(nums):
        if v == 1:
            return False
        while v > 1:
            q = spf[v]
            while v % q == 0:
                v //= q
            if first[q] < 0:
                first[q] = i
            else:
                a = find(parent, i)
                b = find(parent, first[q])
                if a != b:
                    parent[a] = b
                    sets -= 1
    return sets == 1


seed = 2709


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    return next_random() * 32768 + next_random()


def is_smooth(v):
    for p in [2, 3, 5, 7]:
        while v % p == 0:
            v //= p
    return v == 1


smooth = [v for v in range(2, 100001) if is_smooth(v)]

print(str(can_traverse_all_pairs([2, 3, 6])).lower())
print(str(can_traverse_all_pairs([3, 9, 5])).lower())
print(str(can_traverse_all_pairs([4, 3, 12, 8])).lower())
print(str(can_traverse_all_pairs([1])).lower())
print(str(can_traverse_all_pairs([1, 1])).lower())
print(str(can_traverse_all_pairs([2, 3])).lower())
print(str(can_traverse_all_pairs([99991] * 100000)).lower())
print(str(can_traverse_all_pairs(list(range(2, 100002)))).lower())
print(str(can_traverse_all_pairs(list(range(2, 100001, 2)))).lower())
print(str(can_traverse_all_pairs([99998, 99991, 2] + [6] * 10)).lower())
yes = 0
check = 0
for _ in range(2000):
    n = next_random() % 8 + 1
    nums = [next_random() % 30 + 1 for _ in range(n)]
    can = can_traverse_all_pairs(nums)
    yes += can
    check = (check * 31 + (2 if can else 1)) % 1000000007
print(f"2000 cases up to 30: {yes} traversable, checksum {check}")
yes = 0
check = 0
for _ in range(100):
    n = next_random() % 10000 + 1
    if next_random() % 2 == 0:
        nums = [smooth[next_random() % len(smooth)] for _ in range(n)]
    else:
        nums = [wide() % 100000 + 1 for _ in range(n)]
    can = can_traverse_all_pairs(nums)
    yes += can
    check = (check * 31 + (2 if can else 1)) % 1000000007
print(f"100 cases up to 100000: {yes} traversable, checksum {check}, {len(smooth)} smooth numbers")
