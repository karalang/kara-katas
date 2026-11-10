# Benchmark: LeetCode #1090 Largest Values From Labels -- Python mirror of the
# ★ arm: (value, label) pairs sorted by value from the largest (stable, as
# Kāra's `sort_by`), taken while their label has uses left (a dict of uses per
# label). Same workload and sink as largest_values_from_labels.kara.


def largest_vals_from_labels(values, labels, num_wanted, use_limit):
    items = list(zip(values, labels))
    items.sort(key=lambda p: -p[0])
    used = {}
    taken = 0
    total = 0
    for value, label in items:
        if taken == num_wanted:
            break
        uses = used.get(label, 0)
        if uses < use_limit:
            used[label] = uses + 1
            total += value
            taken += 1
    return total


def main():
    seed = 1090

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    problems = []
    for _ in range(100):
        values = []
        labels = []
        for _ in range(20000):
            values.append(next_random() % 20001)
            labels.append(next_random() % 1000)
        problems.append((values, labels))
    total = 0
    check = 0
    for rnd in range(20):
        for k, (values, labels) in enumerate(problems):
            num_wanted = (rnd * 7919 + k * 31) % 20000 + 1
            use_limit = (rnd * 13 + k) % 20 + 1
            answer = largest_vals_from_labels(values, labels, num_wanted, use_limit)
            total += answer
            check = (check * 31 + answer) % 1000000007
    print(f"20 rounds over 100 problems of 2 * 10^4 items: answers sum to {total}, checksum {check}")


main()
