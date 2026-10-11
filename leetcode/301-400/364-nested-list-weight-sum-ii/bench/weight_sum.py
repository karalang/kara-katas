# Benchmark for #364 -- mirror of weight_sum.kara. An integer is an int and
# a list is a Python list.
import sys

sys.setrecursionlimit(10000)


def max_depth(items, depth):
    deepest = 0
    for item in items:
        if isinstance(item, int):
            deepest = max(deepest, depth)
        else:
            deepest = max(deepest, max_depth(item, depth + 1))
    return deepest


def weighted(items, depth, top):
    total = 0
    for item in items:
        if isinstance(item, int):
            total += item * (top - depth + 1)
        else:
            total += weighted(item, depth + 1, top)
    return total


def depth_sum_inverse(items):
    return weighted(items, 1, max_depth(items, 1))


seed = 364


def next_rand():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def build(depth):
    n = next_rand() % 13
    out = []
    for _ in range(n):
        if depth < 14 and next_rand() % 3 == 0:
            out.append(build(depth + 1))
        else:
            out.append(next_rand() % 201 - 100)
    return out


def main():
    checksum = 0
    for _ in range(10):
        items = build(1)
        for _ in range(20):
            checksum = (checksum * 31 + depth_sum_inverse(items) + 1000000000000000) % 1000000007
    print(f"checksum {checksum}")


main()
