# LeetCode #1578 bench: the same one pass, in Python.

seed = 1578


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def min_cost(colors, needed_time):
    total = 0
    keep = 0
    for i in range(len(colors)):
        if i > 0 and colors[i] != colors[i - 1]:
            keep = 0
        total += min(keep, needed_time[i])
        keep = max(keep, needed_time[i])
    return total


def main():
    ropes = []
    for _ in range(200):
        colors = []
        times = []
        for _ in range(100000):
            colors.append(chr(ord("a") + next_random() % 3))
            times.append(next_random() % 1000 + 1)
        ropes.append(("".join(colors), times))
    check = 0
    total = 0
    for colors, times in ropes:
        cost = min_cost(colors, times)
        total += cost
        check = mix(check, cost)
    print(f"200 ropes of 100000 balloons: time total {total}, checksum {check}")


main()
