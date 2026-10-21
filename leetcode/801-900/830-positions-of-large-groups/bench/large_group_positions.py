# Benchmark for #830: Positions of Large Groups -- the ★ arm (two pointers).
#
# Mirrors large_group_positions.kara: from the start i of each group, j
# runs on while the letter stays the same, and the group s[i..j] is kept
# when it holds 3 or more.


def large_group_positions(s):
    n = len(s)
    groups = []
    i = 0
    while i < n:
        j = i
        while j < n and s[j] == s[i]:
            j += 1
        if j - i >= 3:
            groups.append([i, j - 1])
        i = j
    return groups


def main():
    count, rounds, n = 64, 200000, 1000
    seed = 830

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    strings = []
    for g in range(count):
        letters = 1 + g % 3
        strings.append("".join(chr(97 + next_random() % letters) for _ in range(n)))
    total = 0
    checksum = 0
    for rnd in range(rounds):
        groups = large_group_positions(strings[rnd % count])
        total += len(groups)
        for g in groups:
            checksum = (checksum * 131 + g[0] * 1009 + g[1]) % 1000000007
    print(f"{rounds} rounds of {count} strings: {total} groups, checksum {checksum}")


main()
