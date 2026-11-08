# LeetCode #2007: Find Original Array From Doubled Array -- the ★ arm's
# benchmark, a mirror of doubled.kara.


def find_original_array(changed):
    if len(changed) % 2 == 1:
        return []
    top = max(changed)
    count = [0] * (top + 1)
    for x in changed:
        count[x] += 1
    if count[0] % 2 == 1:
        return []
    original = [0] * (count[0] // 2)
    for v in range(1, top + 1):
        c = count[v]
        if c == 0:
            continue
        if 2 * v > top or count[2 * v] < c:
            return []
        count[2 * v] -= c
        for _ in range(c):
            original.append(v)
    return original


seed = 2007


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    arrays = []
    for _ in range(2000):
        changed = []
        for _ in range(500):
            x = next_random() % 5001
            changed.append(x)
            changed.append(2 * x)
        for i in range(len(changed) - 1, 0, -1):
            j = next_random() % (i + 1)
            changed[i], changed[j] = changed[j], changed[i]
        if next_random() % 3 == 0:
            i = next_random() % len(changed)
            changed[i] += 1
        arrays.append(changed)
    calls = 0
    total_sum = 0
    check = 0
    for _ in range(25):
        for a in range(len(arrays)):
            original = find_original_array(arrays[a])
            total = len(original)
            for v in original:
                total += v
            calls += 1
            total_sum += total
            check = (check * 31 + total) % 1000000007
    print(f"{calls} calls: sum {total_sum}, checksum {check}")


main()
