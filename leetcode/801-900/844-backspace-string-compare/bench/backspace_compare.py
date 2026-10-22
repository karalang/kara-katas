# Benchmark for #844: Backspace String Compare -- Python twin of the Kāra ★
# arm (two pointers from the back).


def next_kept(s, i):
    skip = 0
    while i >= 0:
        if s[i] == "#":
            skip += 1
        elif skip > 0:
            skip -= 1
        else:
            return i
        i -= 1
    return -1


def backspace_compare(s, t):
    i = next_kept(s, len(s) - 1)
    j = next_kept(t, len(t) - 1)
    while i >= 0 and j >= 0:
        if s[i] != t[j]:
            return False
        i = next_kept(s, i - 1)
        j = next_kept(t, j - 1)
    return i < 0 and j < 0


def main():
    count, rounds = 64, 3500000
    seed = 844

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    firsts = []
    seconds = []
    for g in range(count):
        k = 2 + g % 3
        cs = []
        for _ in range(120):
            if next_random() % 10 < 3:
                cs.append("#")
            else:
                cs.append(chr(97 + next_random() % k))
        first = "".join(cs)
        for _ in range(40):
            at = next_random() % (len(cs) + 1)
            cs.insert(at, "#")
            cs.insert(at, chr(97 + next_random() % k))
        if g % 2 == 1:
            at = next_random() % len(cs)
            cs[at] = "a" if cs[at] == "#" else "#"
        firsts.append(first)
        seconds.append("".join(cs))
    equal = 0
    checksum = 0
    for rnd in range(rounds):
        g = rnd % count
        same = backspace_compare(firsts[g], seconds[g])
        if same:
            equal += 1
        checksum = (checksum * 31 + (rnd % 1000 if same else 7)) % 1000000007
    print(f"{rounds} rounds of {count} pairs: {equal} equal, checksum {checksum}")


main()
