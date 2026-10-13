# LeetCode #514: Freedom Trail -- dynamic programming over the positions
# of each letter. Mirrors find_rotate_steps.kara (the star arm) and its
# harness.


def find_rotate_steps(ring, key):
    r = ring.encode()
    n = len(r)
    at = [[] for _ in range(26)]
    for j in range(n):
        at[r[j] - ord("a")].append(j)
    prev_pos = [0]
    prev_cost = [0]
    for c in key.encode():
        pos = list(at[c - ord("a")])
        cost = []
        for q in pos:
            best = 2**63 - 1
            for i in range(len(prev_pos)):
                d = abs(prev_pos[i] - q)
                best = min(best, prev_cost[i] + min(d, n - d))
            cost.append(best)
        prev_pos = pos
        prev_cost = cost
    fewest = 2**63 - 1
    for c in prev_cost:
        fewest = min(fewest, c)
    return fewest + len(key)


# ---- test harness ---------------------------------------------------------

seed = 514


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(ring, key):
    print(f'"{ring}", "{key}": {find_rotate_steps(ring, key)}')


def main():
    show("godding", "gd")
    show("godding", "godding")
    show("a", "a")
    show("ab", "bbbb")
    show("abcde", "eae")
    show("caotmcaataijjxi", "oatjiioicitatajtijciocjcaaxaaatmctxamacaamjjx")
    count = 300
    total = 0
    checksum = 0
    for t in range(count):
        letters = 2 if t % 3 == 0 else 5 if t % 3 == 1 else 26
        n = 1 + next_random() % 60
        m = 1 + next_random() % 60
        ring = "".join(chr(ord("a") + next_random() % letters) for _ in range(n))
        key = "".join(ring[next_random() % n] for _ in range(m))
        steps = find_rotate_steps(ring, key)
        total += steps
        checksum = (checksum * 31 + steps) % 1000000007
    print(f"{count} random rings: {total} steps in all, checksum {checksum}")


main()
