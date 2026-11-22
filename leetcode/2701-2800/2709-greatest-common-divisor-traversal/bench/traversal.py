# LeetCode #2709: Greatest Common Divisor Traversal -- the bench
# (traversal.kara in Python): a smallest-prime-factor sieve, and each
# index joined in a union-find to the first index seen with each of its
# primes.


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


arrays, n, rounds = 20, 100000, 5
everything = []
for a in range(arrays):
    nums = []
    for _ in range(n):
        if a % 2 == 0:
            p = [2, 3, 5, 7][next_random() % 4]
            nums.append(p * (wide() % 14285 + 1))
        else:
            nums.append(wide() % 99999 + 2)
    everything.append(nums)
yes = 0
check = 0
for r in range(rounds):
    for nums in everything:
        can = can_traverse_all_pairs(nums)
        yes += can
        check = (check * 31 + (2 if can else 1) + r) % 1000000007
print(f"{arrays} arrays of {n} numbers up to 100000, {rounds} rounds: {yes} traversable, checksum {check}")
