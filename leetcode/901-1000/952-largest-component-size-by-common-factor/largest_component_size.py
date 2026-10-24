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


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


# n distinct numbers from 1 to top, in a random order.
def random_numbers(n, top):
    taken = set()
    out = []
    while len(out) < n:
        v = 1 + (next_random() * 32768 + next_random()) % top
        if v not in taken:
            taken.add(v)
            out.append(v)
    return out


def show(nums):
    return "[" + ",".join(str(v) for v in nums) + "]"


def main():
    global seed
    # LeetCode's three examples, then a few more
    examples = [
        [4, 6, 15, 35],
        [20, 50, 9, 63],
        [2, 3, 6, 7, 4, 12, 21, 39],
        [1],
        [1, 2, 3, 5, 7],
        [6, 10, 15],
        [2, 9, 77, 35],
        [99991, 99989, 2],
    ]
    for e in examples:
        print(f"{show(e)}: {largest_component_size(e)}")
    # 300 random cases of 1 to 12 numbers up to 60
    seed = 952
    count = 0
    total = 0
    check = 0
    for _ in range(300):
        n = 1 + next_random() % 12
        nums = random_numbers(n, 60)
        r = largest_component_size(nums)
        count += n
        total += r
        check = (check * 31 + r) % 1000000007
    print(f"300 random cases of {count} numbers up to 60: largest components adding to {total}, checksum {check}")
    # LeetCode's largest, 20000 numbers up to 100000
    mixed = random_numbers(20000, 100000)
    print(f"20000 random numbers: {largest_component_size(mixed)}")
    odd = [2 * k + 1 for k in range(20000)]
    print(f"the odd numbers 1 to 39999: {largest_component_size(odd)}")
    primes = []
    c = 2
    while len(primes) < 9592:
        prime = True
        d = 2
        while d * d <= c:
            if c % d == 0:
                prime = False
                break
            d += 1
        if prime:
            primes.append(c)
        c += 1
    print(f"the 9592 primes below 100000: {largest_component_size(primes)}")
    evens = [2 * k for k in range(1, 20001)]
    print(f"the even numbers 2 to 40000: {largest_component_size(evens)}")


main()
