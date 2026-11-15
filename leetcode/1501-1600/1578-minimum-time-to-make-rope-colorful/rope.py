# LeetCode #1578: Minimum Time to Make Rope Colorful -- the Python mirror of
# the ★ arm: in each run of one colour every balloon but the slowest to
# remove goes; one pass keeps the largest time of the run so far and pays
# the smaller of that and each later balloon's time. O(n)


def min_cost(colors, needed_time):
    total = 0
    keep = 0
    for i in range(len(colors)):
        if i > 0 and colors[i] != colors[i - 1]:
            keep = 0
        total += min(keep, needed_time[i])
        keep = max(keep, needed_time[i])
    return total


# ---- the harness: the same in every arm

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def batch(count, most, letters, top):
    check = 0
    total = 0
    for _ in range(count):
        n = (next_random() * 32768 + next_random()) % most + 1
        stay = next_random() % 3 + 1
        colors = []
        last = "a"
        for _ in range(n):
            if next_random() % stay != 0:
                last = chr(ord("a") + next_random() % letters)
            colors.append(last)
        colors = "".join(colors)
        times = [(next_random() * 32768 + next_random()) % top + 1 for _ in range(n)]
        cost = min_cost(colors, times)
        total += cost
        check = mix(check, cost)
    print(f"{count} ropes of up to {most} balloons: time total {total}, checksum {check}")


def main():
    global seed
    examples = [
        ("abaac", [1, 2, 3, 4, 5]),
        ("abc", [1, 2, 3]),
        ("aabaa", [1, 2, 3, 4, 1]),
        ("a", [7]),
        ("aaaa", [4, 9, 3, 8]),
        ("bbbaaa", [4, 9, 3, 8, 1, 2]),
    ]
    for colors, times in examples:
        print(f"{colors} {times} -> {min_cost(colors, times)}")
    seed = 1578
    batch(3000, 8, 3, 9)
    batch(300, 1000, 26, 10000)
    batch(30, 100000, 2, 10000)


main()
