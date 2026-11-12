# LeetCode #1131: Maximum of Absolute Value Expression -- the bench in
# Python, the same algorithm and workload as max_abs_val_expr.kara: each
# array its own list, the same 8 pairs of 40000 values and 400 rounds.


def max_abs_val_expr(arr1, arr2):
    best = 0
    for p, q in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
        high = -(1 << 63)
        low = (1 << 63) - 1
        for i in range(len(arr1)):
            v = p * arr1[i] + q * arr2[i] + i
            if v > high:
                high = v
            if v < low:
                low = v
        best = max(best, high - low)
    return best


seed = 1131


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def value():
    high = next_random()
    low = next_random()
    return (high * 32768 + low) % 2000001 - 1000000


def main():
    firsts = []
    seconds = []
    for _ in range(8):
        firsts.append([value() for _ in range(40000)])
        seconds.append([value() for _ in range(40000)])
    total = 0
    check = 0
    for rnd in range(400):
        for j in range(8):
            at = (rnd * 7919 + j * 104729) % 40000
            firsts[j][at] = ((firsts[j][at] + 1000000) * 7 + 12345) % 2000001 - 1000000
            seconds[j][at] = ((seconds[j][at] + 1000000) * 11 + 54321) % 2000001 - 1000000
            r = max_abs_val_expr(firsts[j], seconds[j])
            total += r
            check = (check * 31 + r) % 1000000007
    print(f"400 rounds over 8 pairs of 40000 values: answers total {total}, checksum {check}")


main()
