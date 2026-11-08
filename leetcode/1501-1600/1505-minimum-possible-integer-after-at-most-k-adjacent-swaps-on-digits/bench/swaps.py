# LeetCode #1505: Minimum Possible Integer After at Most K Adjacent Swaps On
# Digits -- the benchmark, the same algorithm as swaps.kara: greedily, each place takes the
# smallest digit whose nearest copy can be brought there with the swaps
# left; a copy's cost is its index less the digits already taken from
# before it, counted by a Fenwick tree.


def min_integer(num, k):
    n = len(num)
    where = [[] for _ in range(10)]
    for i, c in enumerate(num):
        where[ord(c) - 48].append(i)
    head = [0] * 10
    tree = [0] * (n + 1)

    def taken_before(i):
        s = 0
        while i > 0:
            s += tree[i]
            i -= i & -i
        return s

    def take(i):
        i += 1
        while i <= n:
            tree[i] += 1
            i += i & -i

    out = []
    for _ in range(n):
        for d in range(10):
            if head[d] < len(where[d]):
                i = where[d][head[d]]
                cost = i - taken_before(i)
                if cost <= k:
                    k -= cost
                    head[d] += 1
                    take(i)
                    out.append(chr(48 + d))
                    break
    return "".join(out)


seed = 1505


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def main():
    cases = []
    for c in range(60):
        digits = c % 10 + 1
        num = "".join(chr(48 + next_random() % digits) for _ in range(30000))
        cases.append((num, next_random() * (c % 7 + 1) * 50))
    check = 0
    for num, k in cases:
        for ch in min_integer(num, k):
            check = mix(check, ord(ch) - 48)
    print(f"60 numbers of 30000 digits: checksum {check}")


main()
