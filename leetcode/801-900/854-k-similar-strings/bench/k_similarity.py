# Benchmark for #854: K-Similar Strings -- Python twin of the Kāra ★ arm
# (breadth-first search over swaps that fix a letter).


def k_similarity(s1, s2):
    goal = s2.encode()
    n = len(goal)
    seen = {s1}
    level = [bytearray(s1.encode())]
    swaps = 0
    while True:
        nxt = []
        for cur in level:
            i = 0
            while i < n and cur[i] == goal[i]:
                i += 1
            if i == n:
                return swaps
            for j in range(i + 1, n):
                if cur[j] == goal[i] and cur[j] != goal[j]:
                    moved = bytearray(cur)
                    moved[i], moved[j] = moved[j], moved[i]
                    key = moved.decode()
                    if key not in seen:
                        seen.add(key)
                        nxt.append(moved)
        level = nxt
        swaps += 1


seed = 854


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count = 64
    rounds = 6400
    n = 20
    firsts = []
    seconds = []
    for g in range(count):
        letters = 2 + g % 5
        a = [ord("a") + next_random() % letters for _ in range(n)]
        b = list(a)
        for i in range(n - 1, 0, -1):
            j = next_random() % (i + 1)
            b[i], b[j] = b[j], b[i]
        firsts.append(bytes(a).decode())
        seconds.append(bytes(b).decode())
    total = 0
    checksum = 0
    for round_ in range(rounds):
        g = round_ % count
        k = k_similarity(firsts[g], seconds[g])
        total += k
        checksum = (checksum * 31 + k) % 1000000007
    print(f"{rounds} rounds of {count} pairs: swaps sum to {total}, checksum {checksum}")


main()
