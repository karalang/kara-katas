# LeetCode #401: Binary Watch -- mirror of binary_watch.kara (try every time).


def ones(x):
    count = 0
    y = x
    while y > 0:
        count += y % 2
        y = y // 2
    return count


def read_binary_watch(turned_on):
    return [f"{h}:{m:02}" for h in range(12) for m in range(60) if ones(h) + ones(m) == turned_on]


def digest(times):
    h = 0
    for i, t in enumerate(times):
        if i > 0:
            h = (h * 131 + 44) % 1000000007
        for b in t.encode():
            h = (h * 131 + b) % 1000000007
    return h


def main():
    for n in range(11):
        times = read_binary_watch(n)
        if len(times) <= 10:
            print(f"{n} LEDs: {len(times)} times [{', '.join(times)}]")
        else:
            print(f"{n} LEDs: {len(times)} times, first {times[0]}, last {times[-1]}, digest {digest(times)}")


main()
