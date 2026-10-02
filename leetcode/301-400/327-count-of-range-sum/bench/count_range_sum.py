"""Benchmark workload for LeetCode #327 — Python mirror of count_range_sum.kara."""

LEN = 100000
PUNCHES = 20
MODULUS = 1073741789


def count_and_sort(p, tmp, lo, hi, lower, upper):
    if hi - lo <= 1:
        return 0
    mid = lo + (hi - lo) // 2
    count = count_and_sort(p, tmp, lo, mid, lower, upper) + count_and_sort(p, tmp, mid, hi, lower, upper)
    start = end = mid
    for a in range(lo, mid):
        while start < hi and p[start] < p[a] + lower:
            start += 1
        while end < hi and p[end] <= p[a] + upper:
            end += 1
        count += end - start
    i, j, k = lo, mid, lo
    while i < mid and j < hi:
        if p[i] <= p[j]:
            tmp[k] = p[i]
            i += 1
        else:
            tmp[k] = p[j]
            j += 1
        k += 1
    while i < mid:
        tmp[k] = p[i]
        i += 1
        k += 1
    while j < hi:
        tmp[k] = p[j]
        j += 1
        k += 1
    for t in range(lo, hi):
        p[t] = tmp[t]
    return count


def count_range_sum(nums, lower, upper):
    p = [0]
    s = 0
    for x in nums:
        s += x
        p.append(s)
    tmp = [0] * len(p)
    return count_and_sort(p, tmp, 0, len(p), lower, upper)


class Seed:
    def __init__(self, v):
        self.v = v

    def next(self):
        self.v = (self.v * 1103515245 + 12345) % 2147483648
        return self.v // 65536


def main():
    seed = Seed(327)
    a = [seed.next() % 2001 - 1000 for _ in range(LEN)]
    sink = 0
    for _ in range(PUNCHES):
        pos = (seed.next() * 32768 + seed.next()) % LEN
        a[pos] = seed.next() % 2001 - 1000
        w = seed.next() % 1000
        count = count_range_sum(a, -w, w)
        sink = (sink * 31 + count % MODULUS) % MODULUS
    print(f"sink {sink}")


main()
