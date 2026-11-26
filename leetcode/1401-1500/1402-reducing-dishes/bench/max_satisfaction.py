# LeetCode #1402 bench, Python: the same sort and running sum, workload
# and checksum as max_satisfaction.kara.


def max_satisfaction(satisfaction):
    order = sorted(satisfaction, reverse=True)
    running = 0
    total = 0
    for s in order:
        if running + s <= 0:
            break
        running += s
        total += running
    return total


def main():
    seed = 1402
    pool = []
    for _ in range(100000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        pool.append(seed % 2001 - 1000)
    check = 0
    for r in range(20000):
        at = (check + r * 7919) % 99501
        window = pool[at:at + 500]
        check = (check * 131 + max_satisfaction(window)) % 1000000007
    print(f"20000 windows of 500 dishes: checksum {check}")


main()
