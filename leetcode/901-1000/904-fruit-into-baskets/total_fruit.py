# LeetCode #904: Fruit Into Baskets -- Python mirror of the sliding window
# over a map of counts in total_fruit.kara, with the same test harness.
#
# Move the stretch's right end one tree at a time, counting each type in
# it; while the counts hold three types, move the left end on, dropping a
# type whose count reaches 0. The longest stretch seen is the answer.
# O(n).


def total_fruit(fruits):
    counts = {}
    left = 0
    best = 0
    for right in range(len(fruits)):
        f = fruits[right]
        counts[f] = counts.get(f, 0) + 1
        while len(counts) > 2:
            g = fruits[left]
            c = counts.get(g, 0) - 1
            if c == 0:
                del counts[g]
            else:
                counts[g] = c
            left += 1
        best = max(best, right - left + 1)
    return best


# ---- test harness ----------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(fruits):
    listed = ",".join(str(f) for f in fruits)
    print(f"fruits = [{listed}] -> {total_fruit(fruits)}")


# `len` trees of types below `kinds` (and below `len`), in runs of up to
# `run` trees of one type
def random_trees(length, kinds, run):
    out = []
    k = min(kinds, length)
    while len(out) < length:
        f = next_random() % k
        r = 1 + next_random() % run
        for _ in range(r):
            if len(out) < length:
                out.append(f)
    return out


def main():
    global seed
    show([1, 2, 1])
    show([0, 1, 2, 2])
    show([1, 2, 3, 2, 2])
    show([3, 3, 3, 1, 2, 1, 1, 2, 3, 3, 4])
    show([0])
    show([0, 0, 0, 0])
    show([0, 1, 0, 1, 0, 1])
    show([0, 1, 2, 3, 4, 5])
    show([1, 0, 1, 4, 1, 4, 1, 2, 3])
    # random cases of up to 1000 trees, from 2 types to as many as trees,
    # in runs of up to 1 to 5 trees
    seed = 904
    check = 0
    total = 0
    for c in range(300):
        length = 1 + next_random() % 1000
        kinds = 2 if c % 4 == 0 else 3 if c % 4 == 1 else 5 if c % 4 == 2 else length
        got = total_fruit(random_trees(length, kinds, 1 + c % 5))
        total += got
        check = (check * 1000003 + got) % 1000000007
    print(f"300 cases: answers summing to {total}, checksum {check}")
    # LeetCode's largest: 10^5 trees of 3 types in runs of up to 50, and
    # 10^5 trees of 2 types with a third every 30000
    print(f"100000 trees of 3 types -> {total_fruit(random_trees(100000, 3, 50))}")
    two = [2 if i % 30000 == 29999 else i % 2 for i in range(100000)]
    print(f"100000 trees of 2 types, a third every 30000 -> {total_fruit(two)}")


main()
