# Benchmark for #849: Maximize Distance to Closest Person -- Python twin of
# the Kāra ★ arm (one pass, remembering the last person).


def max_dist_to_closest(seats):
    n = len(seats)
    last = -1
    best = 0
    for i in range(n):
        if seats[i] == 1:
            if last < 0:
                best = i
            else:
                best = max(best, (i - last) // 2)
            last = i
    return max(best, n - 1 - last)


seed = 849


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count = 64
    rounds = 20000
    n = 20000
    rows = []
    for g in range(count):
        odds = 2 << (g % 8)
        seats = [1 if next_random() % odds == 0 else 0 for _ in range(n)]
        taken = next_random() % n
        empty = (taken + 1 + next_random() % (n - 1)) % n
        seats[taken] = 1
        seats[empty] = 0
        rows.append(seats)
    total = 0
    checksum = 0
    for round_ in range(rounds):
        d = max_dist_to_closest(rows[round_ % count])
        total += d
        checksum = (checksum * 31 + d) % 1000000007
    print(f"{rounds} rounds of {count} rows: distances sum to {total}, checksum {checksum}")


main()
