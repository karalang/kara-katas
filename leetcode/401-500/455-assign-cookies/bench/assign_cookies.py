# Benchmark for #455: mirror of assign_cookies.kara (the ★ arm, both
# sorted, least greedy child first) on the same workload.


def find_content_children(g, s):
    greed = sorted(g)
    sizes = sorted(s)
    child = 0
    for size in sizes:
        if child < len(greed) and size >= greed[child]:
            child += 1
    return child


# ---- benchmark --------------------------------------------------------

seed = 455


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_value():
    hi = next_random()
    lo = next_random()
    return 1 + (hi * 65536 + lo) % 1000000000


def main():
    n = 1000000
    rounds = 10
    g = []
    s = []
    for _ in range(n):
        g.append(random_value())
        s.append(random_value())
    total = 0
    checksum = 0
    for _ in range(rounds):
        hi = next_random()
        lo = next_random()
        g[(hi * 65536 + lo) % n] = random_value()
        hi = next_random()
        lo = next_random()
        s[(hi * 65536 + lo) % n] = random_value()
        fed = find_content_children(g, s)
        total += fed
        checksum = (checksum * 31 + fed) % 1000000007
    print(f"{rounds} rounds on {n} children and {n} cookies: {total} content, checksum {checksum}")


main()
