# LeetCode #2813: Maximum Elegance of a K-Length Subsequence -- the Python
# mirror of the ★ arm: the k dearest items taken, then each later item of
# a new category swapped in for the cheapest repeat, the best kept.


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


def random_items(n, top, kinds):
    items = []
    for _ in range(n):
        profit = wide() % top + 1
        category = wide() % kinds + 1
        items.append([profit, category])
    return items


def main():
    print(find_maximum_elegance([[3, 2], [5, 1], [10, 1]], 2))
    print(find_maximum_elegance([[3, 1], [3, 1], [2, 2], [5, 3]], 3))
    print(find_maximum_elegance([[1, 1], [2, 1], [3, 1]], 3))
    print(find_maximum_elegance([[p * 1000000, 7] for p in range(1, 1001)], 500))
    print(find_maximum_elegance([[1000000000, c] for c in range(1, 1001)], 1000))
    check = 0
    for _ in range(3000):
        n = next_random() % 8 + 1
        items = random_items(n, 10, n)
        k = next_random() % n + 1
        check = (check * 31 + find_maximum_elegance(items, k)) % 1000000007
    print(f"3000 small cases: checksum {check}")
    check = 0
    for _ in range(50):
        n = wide() % 1000 + 1
        items = random_items(n, 1000000000, n)
        k = wide() % n + 1
        check = (check * 31 + find_maximum_elegance(items, k)) % 1000000007
    print(f"50 large cases: checksum {check}")


main()
