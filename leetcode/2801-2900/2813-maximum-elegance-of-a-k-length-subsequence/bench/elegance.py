# LeetCode #2813: Maximum Elegance of a K-Length Subsequence -- the bench
# in Python: the ★ arm over 10 cases of 10^5 items, profits up to 10^9
# and categories up to 30000, k from 1 to 10^5, all drawn first, then
# each answered 5 times.


def find_maximum_elegance(items, k):
    order = sorted(items, key=lambda it: -it[0])
    seen = set()
    repeats = []
    total = 0
    for profit, category in order[:k]:
        total += profit
        if category in seen:
            repeats.append(profit)
        else:
            seen.add(category)
    best = total + len(seen) * len(seen)
    for profit, category in order[k:]:
        if not repeats:
            break
        if category not in seen:
            seen.add(category)
            total += profit - repeats.pop()
            best = max(best, total + len(seen) * len(seen))
    return best


seed = 2813


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def main():
    count, rounds, n = 10, 5, 100000
    cases = []
    for _ in range(count):
        items = []
        for _ in range(n):
            profit = wide() % 1000000000 + 1
            category = wide() % 30000 + 1
            items.append([profit, category])
        cases.append((items, wide() % n + 1))
    total = 0
    check = 0
    for r in range(rounds):
        for items, k in cases:
            a = find_maximum_elegance(items, k)
            total += a
            check = (check * 31 + a % 1000000007 + r) % 1000000007
    print(f"{count} cases of {n}, {rounds} rounds: elegance sums to {total}, checksum {check}")


main()
