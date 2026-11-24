# LeetCode #1331: Rank Transform of an Array -- Python mirror of the ★ arm
# and its harness.
from bisect import bisect_left


def array_rank_transform(arr):
    distinct = sorted(set(arr))
    return [bisect_left(distinct, x) + 1 for x in arr]


seed = 1331


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def fold(check, ranks):
    c = check
    for r in ranks:
        c = (c * 131 + r) % 1000000007
    return (c * 131 + 7) % 1000000007


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    f = array_rank_transform
    print(f"{show(f([40, 10, 20, 30]))} {show(f([100, 100, 100]))} {show(f([37, 12, 28, 9, 100, 56, 80, 5, 12]))}")
    print(f"{show(f([]))} {show(f([1000000000, -1000000000, 0, -1000000000]))}")
    long = [50000 - i // 2 for i in range(100000)]
    ranks = f(long)
    print(f"10^5 values: first {ranks[0]}, last {ranks[99999]}, checksum {fold(0, ranks)}")
    check = 0
    most = 0
    for t in range(600):
        n = next_random() % 3001 if t % 10 == 0 else next_random() % 13
        arr = []
        for _ in range(n):
            if t % 3 == 0:
                v = next_random() % 3
            elif t % 3 == 1:
                v = next_random() % 1000 - 500
            else:
                a = next_random()
                b = next_random()
                v = (a * 61036 + b) % 2000000001 - 1000000000
            arr.append(v)
        ranks = f(arr)
        for r in ranks:
            most = max(most, r)
        check = fold(check, ranks)
    print(f"600 random arrays: highest rank {most}, checksum {check}")


main()
