"""Benchmark workload — Remove Duplicates from Sorted Array II (LeetCode #80).

Python mirror of bench/remove_duplicates_ii.kara. The generalized run-scan computes
the at-most-2 dedup and folds each kept value through a rolling polynomial hash. Runs
a smaller K (pure-Python is slow); timed separately, NOT cross-checked. See
../README.md.
"""


def build(n):
    arr = []
    val = 0
    pos = 0
    while pos < n:
        runlen = (val % 3) + 1
        r = 0
        while r < runlen and pos < n:
            arr.append(val)
            pos += 1
            r += 1
        val += 1
    return arr


def scan_fold(arr, n, seed):
    acc = seed
    i = 0
    while i < n:
        v = arr[i]
        run = 0
        while i < n and arr[i] == v:
            if run < 2:
                acc = (acc * 131 + (v + 1)) % 1000000007
            run += 1
            i += 1
    return acc


def main():
    n = 3000
    total = 3000
    modulus = 1000000007
    arr = build(n)
    total_sum = 0
    for it in range(total):
        r = scan_fold(arr, n, it)
        total_sum = (total_sum + r) % modulus
    print(total_sum)


if __name__ == "__main__":
    main()
