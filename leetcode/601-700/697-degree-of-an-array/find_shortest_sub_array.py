# LeetCode #697: Degree of an Array -- first, last and count.
#
# A mirror of find_shortest_sub_array.kara (the ★ arm) and its harness.


def find_shortest_sub_array(nums):
    count, first, last = {}, {}, {}
    for i, x in enumerate(nums):
        if x not in first:
            first[x] = i
        last[x] = i
        count[x] = count.get(x, 0) + 1
    degree = 0
    best = len(nums)
    for x, c in count.items():
        span = last[x] - first[x] + 1
        if c > degree or (c == degree and span < best):
            degree = c
            best = span
    return best


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    global seed
    f = find_shortest_sub_array
    print(f"example 1: {f([1, 2, 2, 3, 1])}")
    print(f"example 2: {f([1, 2, 2, 3, 1, 4, 2])}")
    print(f"one: {f([7])}, all distinct: {f([5, 4, 3, 2, 1])}, tied: {f([1, 2, 1, 3, 3, 4, 2, 5, 2, 1])}, ends: {f([49999, 0, 1, 0, 2, 49999, 49999])}")
    every = list(range(50000))
    mirror = [i if i < 25000 else 49999 - i for i in range(50000)]
    print(f"one value 50000 times: {f([3] * 50000)}, every value once: {f(every)}, mirrored: {f(mirror)}")
    seed = 697
    total = 0
    checksum = 0
    for _ in range(100):
        n = 1 + next_random() % 20000
        rng = 1 + (next_random() * 65536 + next_random()) % 50000
        nums = [(next_random() * 65536 + next_random()) % rng for _ in range(n)]
        r = f(nums)
        total += r
        checksum = (checksum * 31 + r) % 1000000007
    print(f"100 random arrays: shortest spans sum to {total}, checksum {checksum}")


main()
