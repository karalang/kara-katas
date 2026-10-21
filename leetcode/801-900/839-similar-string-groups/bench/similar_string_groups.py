# Benchmark for #839: Similar String Groups -- the ★ arm (union-find).
#
# Mirrors similar_string_groups.kara: every pair of words is compared
# once, stopping at a third difference, and a pair that differs in no
# position or in two joins its two groups, kept as a union-find forest
# with path halving. As in the Kāra program, each word is copied out to
# its own bytes for every count.


def similar(a, b):
    diff = 0
    for k in range(len(a)):
        if a[k] != b[k]:
            diff += 1
            if diff > 2:
                return False
    return diff != 1


def find(parent, x):
    v = x
    while parent[v] != v:
        parent[v] = parent[parent[v]]
        v = parent[v]
    return v


def num_similar_groups(strs):
    words = [s.encode() for s in strs]
    n = len(words)
    parent = list(range(n))
    groups = n
    for i in range(n):
        for j in range(i + 1, n):
            a = find(parent, i)
            b = find(parent, j)
            if a != b and similar(words[i], words[j]):
                parent[a] = b
                groups -= 1
    return groups


seed = 839


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # 16 cases drawn once, each LeetCode's most and longest words, 300 of
    # 300 letters. The first word of case g is random; each later one is
    # an earlier word with one swap, or with three once in 1 + g % 4
    # words. Each round counts the groups of the next case.
    count, rounds, n, m = 16, 500, 300, 300
    cases = []
    for g in range(count):
        jump = 1 + g % 4
        words = [[97 + next_random() % 26 for _ in range(m)]]
        for _ in range(1, n):
            frm = next_random() % len(words)
            swaps = 3 if next_random() % jump == 0 else 1
            w = list(words[frm])
            for _ in range(swaps):
                p = next_random() % m
                q = next_random() % m
                w[p], w[q] = w[q], w[p]
            words.append(w)
        cases.append([bytes(w).decode() for w in words])
    total = 0
    checksum = 0
    for round in range(rounds):
        groups = num_similar_groups(cases[round % count])
        total += groups
        checksum = (checksum * 31 + groups + round) % 1000000007
    print(f"{rounds} rounds of {count} cases: {total} groups, checksum {checksum}")


main()
