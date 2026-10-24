# LeetCode #952 bench: Python mirror of largest_component_size.kara (the ★
# arm, union by prime) on the same 20 sets.
#
# LeetCode #952: Largest Component Size by Common Factor -- union by prime.
#
# Two numbers are joined when they share a factor above 1, and so when
# they share a prime. Factor each number by trial division and join it to
# the first number seen with each of its primes, in a disjoint-set forest
# over the numbers' places; the largest set is the answer. Joining through
# primes never joins two numbers without a common chain of shared primes,
# and every shared prime joins. O(n sqrt(m)) time for numbers up to m.


def find(parent, x):
    root = x
    while parent[root] != root:
        root = parent[root]
    y = x
    while parent[y] != root:
        nxt = parent[y]
        parent[y] = root
        y = nxt
    return root


def largest_component_size(nums):
    n = len(nums)
    parent = list(range(n))
    size = [1] * n
    # first[p]: the first place whose number has the prime p
    first = {}
    for i in range(n):
        x = nums[i]
        p = 2
        while x > 1:
            if p * p > x:
                p = x
            if x % p == 0:
                while x % p == 0:
                    x //= p
                if p in first:
                    a = find(parent, i)
                    b = find(parent, first[p])
                    if a != b:
                        if size[a] < size[b]:
                            parent[a] = b
                            size[b] += size[a]
                        else:
                            parent[b] = a
                            size[a] += size[b]
                else:
                    first[p] = i
            p += 1
    best = 0
    for i in range(n):
        if parent[i] == i and size[i] > best:
            best = size[i]
    return best


# ---- bench ----------------------------------------------------------------

seed = 952


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rounds, count, n = 40, 20, 2000
    # 20 sets of 2000 distinct numbers from 1 to 100000
    sets = []
    for _ in range(count):
        taken = set()
        nums = []
        while len(nums) < n:
            hi = next_random()
            v = 1 + (hi * 32768 + next_random()) % 100000
            if v not in taken:
                taken.add(v)
                nums.append(v)
        sets.append(nums)
    total = 0
    check = 0
    for r in range(rounds):
        for i in range(count):
            k = (r + i) % count
            size = largest_component_size(sets[k])
            total += size
            check = (check * 31 + size) % 1000000007
    print(f"{rounds} rounds over {count} sets of {n} numbers up to 100000: largest components adding to {total}, checksum {check}")


main()
