# LeetCode #1229 bench: the ★ arm in Python, over the same 50 pairs of
# schedules and 10 durations as the Kāra bench.


def min_available_duration(slots1, slots2, duration):
    a = sorted(slots1)
    b = sorted(slots2)
    i = j = 0
    while i < len(a) and j < len(b):
        start = max(a[i][0], b[j][0])
        end = min(a[i][1], b[j][1])
        if end - start >= duration:
            return [start, start + duration]
        if a[i][1] < b[j][1]:
            i += 1
        else:
            j += 1
    return []


def main():
    seed = 1229

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    def slots(count, width, gap):
        out = []
        at = next_random() % (gap + 1)
        for _ in range(count):
            end = at + next_random() % width + 1
            out.append([at, end])
            at = end + next_random() % gap + 1
        for i in range(len(out) - 1, 0, -1):
            j = next_random() % (i + 1)
            out[i], out[j] = out[j], out[i]
        return out

    pairs = []
    for _ in range(50):
        a = slots(10000, 50000, 50000)
        b = slots(10000, 50000, 50000)
        pairs.append((a, b))
    check = 0
    for a, b in pairs:
        for k in range(1, 11):
            answer = min_available_duration(a, b, k * 4000)
            v = 7 if not answer else answer[0]
            check = (check * 131 + v) % 1000000007
    print(f"50 pairs of 10^4 slots, 10 durations: checksum {check}")


main()
