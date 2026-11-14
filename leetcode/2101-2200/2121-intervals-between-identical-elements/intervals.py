# LeetCode #2121: Intervals Between Identical Elements -- the mirror of
# intervals.kara: each value's indices gathered in a dict, then one
# running sum over each list answers every index.


def get_distances(arr):
    positions = {}
    for i, v in enumerate(arr):
        positions.setdefault(v, []).append(i)
    answer = [0] * len(arr)
    for p in positions.values():
        c = len(p)
        total = sum(p)
        before = 0
        for k in range(c):
            after = total - before - p[k]
            answer[p[k]] = k * p[k] - before + after - (c - k - 1) * p[k]
            before += p[k]
    return answer


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def show(xs):
    return "[" + ", ".join(str(x) for x in xs) + "]"


def main():
    examples = [
        [2, 1, 3, 1, 2, 3, 3],
        [10, 5, 10, 10],
        [7],
        [1, 2, 3, 4, 5],
        [4, 4, 4, 4, 4, 4],
        [1, 2, 1, 2, 1, 2, 1],
    ]
    for arr in examples:
        print(f"{show(arr)} -> {show(get_distances(arr))}")
    seed = [2121]
    total = 0
    check = 0
    for rnd in range(2000):
        n = next_random(seed) % 40 + 1
        top = [1, 3, 10, 100000][rnd % 4]
        arr = [next_random(seed) % top + 1 for _ in range(n)]
        for d in get_distances(arr):
            total += d
            check = (check * 31 + d) % 1000000007
    print(f"2000 arrays: distances sum to {total}, checksum {check}")
    far = get_distances([5] * 100000)
    print(f"100000 equal: first {far[0]}, middle {far[50000]}, last {far[99999]}")
    spread = get_distances([i % 7 + 1 for i in range(100000)])
    print(f"100000 in a cycle of 7: sum {sum(spread)}, first {spread[0]}, last {spread[99999]}")


main()
