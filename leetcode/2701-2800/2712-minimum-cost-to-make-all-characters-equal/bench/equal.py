# LeetCode #2712: Minimum Cost to Make All Characters Equal -- the bench
# (equal.kara in Python): each boundary between unequal neighbours priced
# at the cheaper flip across it.


def minimum_cost(s):
    n = len(s)
    cost = 0
    for i in range(1, n):
        if s[i] != s[i - 1]:
            cost += min(i, n - i)
    return cost


seed = 2712


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


count, rounds = 100, 5
strings = []
for _ in range(count):
    change = next_random() % 9
    bits = []
    last = "0"
    for _ in range(100000):
        if next_random() % 8 < change:
            last = "1" if last == "0" else "0"
        bits.append(last)
    strings.append("".join(bits))
total = 0
check = 0
for r in range(rounds):
    for s in strings:
        cost = minimum_cost(s)
        total += cost
        check = (check * 31 + cost + r) % 1000000007
print(f"{count} strings of 100000 bits, {rounds} rounds: costs sum to {total}, checksum {check}")
