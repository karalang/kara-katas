# LeetCode #1505: Minimum Possible Integer After at Most K Adjacent Swaps On
# Digits -- the Python mirror of the ★ arm: greedily, each place takes the
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


def random_case(most_n, most_k):
    n = next_random() % most_n + 1
    digits = next_random() % 10 + 1
    num = "".join(chr(48 + next_random() % digits) for _ in range(n))
    return num, next_random() % (most_k + 1)


def batch(count, most_n, most_k):
    check = 0
    for _ in range(count):
        num, k = random_case(most_n, most_k)
        for c in min_integer(num, k):
            check = mix(check, ord(c) - 48)
    print(f"{count} numbers of 1 to {most_n} digits, k up to {most_k}: checksum {check}")


def main():
    examples = [("4321", 4), ("100", 1), ("36789", 1000), ("22", 22),
                ("9438957234785635408", 23), ("5", 0), ("54321", 10), ("1032", 2)]
    for num, k in examples:
        print(f"{num}, k = {k} -> {min_integer(num, k)}")
    batch(3000, 8, 30)
    batch(300, 200, 3000)
    batch(3, 1500, 1000000)


main()
