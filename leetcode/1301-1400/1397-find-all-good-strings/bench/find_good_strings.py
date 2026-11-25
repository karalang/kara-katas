# LeetCode #1397 bench -- Python: the strings built a letter at a time,
# counted by how much of `evil` their end matches and whether they are
# still at s1's prefix and at s2's, the matches stepped through a KMP
# automaton table.


def slot(j, low, high):
    return j * 4 + (2 if low else 0) + (1 if high else 0)


def find_good_strings(n, s1, s2, evil):
    modulus = 1000000007
    lo = s1.encode()
    hi = s2.encode()
    e = evil.encode()
    m = len(e)
    border = [0] * m
    k = 0
    for i in range(1, m):
        while k > 0 and e[i] != e[k]:
            k = border[k - 1]
        if e[i] == e[k]:
            k += 1
        border[i] = k
    nxt = [0] * (m * 26)
    for j in range(m):
        for c in range(26):
            if e[j] == 97 + c:
                nxt[j * 26 + c] = j + 1
            elif j > 0:
                nxt[j * 26 + c] = nxt[border[j - 1] * 26 + c]
    ways = [0] * (m * 4)
    ways[slot(0, True, True)] = 1
    for i in range(n):
        after = [0] * (m * 4)
        for j in range(m):
            for low in (False, True):
                for high in (False, True):
                    w = ways[slot(j, low, high)]
                    if w == 0:
                        continue
                    first = lo[i] - 97 if low else 0
                    last = hi[i] - 97 if high else 25
                    for c in range(first, last + 1):
                        to = nxt[j * 26 + c]
                        if to == m:
                            continue
                        at = slot(to, low and c == first, high and c == last)
                        after[at] = (after[at] + w) % modulus
        ways = after
    total = 0
    for w in ways:
        total = (total + w) % modulus
    return total


def main():
    seed = 1397

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    low = [chr(97 + next_random() % 3) for _ in range(500)]
    high = [chr(120 + next_random() % 3) for _ in range(500)]
    evil = [chr(97 + next_random() % 3) for _ in range(50)]
    check = 0
    for _ in range(200):
        seed = (seed + check) % 2147483648
        at = next_random() % 500
        low[at] = chr(97 + next_random() % 3)
        at = next_random() % 500
        high[at] = chr(120 + next_random() % 3)
        at = next_random() % 50
        evil[at] = chr(97 + next_random() % 3)
        check = (check * 131 + find_good_strings(500, "".join(low), "".join(high), "".join(evil))) % 1000000007
    print(f"200 rounds at n = 500, evil of 50 letters: checksum {check}")


main()
