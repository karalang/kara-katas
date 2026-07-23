"""Benchmark workload for LeetCode #179 — Largest Number (Python; scale lane)."""


def num_digits(x):
    d = 1
    t = x
    while t >= 10:
        d += 1
        t //= 10
    return d


def pow10(k):
    r = 1
    for _ in range(k):
        r *= 10
    return r


def concat_val(a, b):
    return a * pow10(num_digits(b)) + b


def sort_desc(arr, n):
    for i in range(1, n):
        j = i
        while j > 0 and concat_val(arr[j - 1], arr[j]) < concat_val(arr[j], arr[j - 1]):
            arr[j - 1], arr[j] = arr[j], arr[j - 1]
            j -= 1


def checksum(arr, n):
    modv = 1000000007
    cs = 0
    for i in range(n):
        x = arr[i]
        p = pow10(num_digits(x) - 1)
        while p > 0:
            d = (x // p) % 10
            cs = (cs * 10 + d) % modv
            p //= 10
    return cs


def main():
    n = 500
    passes = 400
    base = [0] * n
    state = 12345
    for c in range(n):
        state = (state * 1103515245 + 12345) & 2147483647
        base[c] = state % 1000
    arr = [0] * n
    sink = 0
    for p in range(passes):
        for k in range(n):
            arr[k] = base[k]
        idx = p % n
        arr[idx] = (arr[idx] + p + 1) % 1000
        sort_desc(arr, n)
        sink += checksum(arr, n)
    print(sink)


main()
