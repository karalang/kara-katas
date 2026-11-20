# LeetCode #1229: Meeting Scheduler -- Python mirror of the ★ arm: both
# people's slots sorted by start, then two pointers.


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


# ---- test harness ---------------------------------------------------------

def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def slots(seed, count, width, gap):
    out = []
    at = next_random(seed) % (gap + 1)
    for _ in range(count):
        end = at + next_random(seed) % width + 1
        out.append([at, end])
        at = end + next_random(seed) % gap + 1
    for i in range(len(out) - 1, 0, -1):
        j = next_random(seed) % (i + 1)
        out[i], out[j] = out[j], out[i]
    return out


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    print(show(min_available_duration([[10, 50], [60, 120], [140, 210]], [[0, 15], [60, 70]], 8)))
    print(show(min_available_duration([[10, 50], [60, 120], [140, 210]], [[0, 15], [60, 70]], 12)))
    print(show(min_available_duration([[5, 9]], [[0, 9]], 4)))
    print(show(min_available_duration([[0, 5]], [[5, 10]], 1)))
    seed = [1229]
    check = 0
    none = 0
    for _ in range(1000):
        a = slots(seed, next_random(seed) % 30 + 1, 40, 40)
        b = slots(seed, next_random(seed) % 30 + 1, 40, 40)
        duration = next_random(seed) % 20 + 1
        answer = min_available_duration(a, b, duration)
        if not answer:
            none += 1
            check = (check * 131 + 7) % 1000000007
        else:
            check = (check * 131 + answer[0] * 3 + answer[1]) % 1000000007
    print(f"1000 random pairs: checksum {check}, {none} with no time")
    a = slots(seed, 10000, 50000, 50000)
    b = slots(seed, 10000, 50000, 50000)
    print(f"10^4 slots each: {show(min_available_duration(a, b, 30000))}, {show(min_available_duration(a, b, 49000))}, {show(min_available_duration(a, b, 1000000))}")


main()
