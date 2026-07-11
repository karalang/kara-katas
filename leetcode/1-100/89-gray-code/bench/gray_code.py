"""Benchmark workload — Gray Code (LeetCode #89).

Python mirror of bench/gray_code.kara. Folds each gray code i ^ (i >> 1) through a
rolling polynomial hash (loop-carried, iter-mixed), smaller K (pure-Python is slow);
timed separately, NOT cross-checked. See ../README.md.
"""


def main():
    n = 65536
    total = 120
    modulus = 1000000007
    total_sum = 0
    for it in range(total):
        acc = it
        for i in range(n):
            g = i ^ (i >> 1)
            acc = (acc * 131 + (g ^ it)) % modulus
        total_sum = (total_sum * 131 + acc) % modulus
    print(total_sum)


if __name__ == "__main__":
    main()
