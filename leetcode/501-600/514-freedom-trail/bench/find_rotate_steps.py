# Benchmark for #514: Python mirror of the ★ arm (a cost per position of
# the current letter); see find_rotate_steps.kara.


def find_rotate_steps(ring, key):
    n = len(ring)
    at = [[] for _ in range(26)]
    for j in range(n):
        at[ring[j] - 97].append(j)
    prev_pos = [0]
    prev_cost = [0]
    for c in key:
        pos = list(at[c - 97])
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


seed = 514


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # 400 random rings of 300 letters from all 26, each with a key of
    # 2,000 letters drawn from the ring, solved once each.
    rings = 400
    total = 0
    checksum = 0
    for _ in range(rings):
        ring = bytes(97 + next_random() % 26 for _ in range(300))
        key = bytes(ring[next_random() % 300] for _ in range(2000))
        steps = find_rotate_steps(ring, key)
        total += steps
        checksum = (checksum * 31 + steps) % 1000000007
    print(f"{rings} rings of 300 letters, keys of 2000: {total} steps in all, checksum {checksum}")


main()
