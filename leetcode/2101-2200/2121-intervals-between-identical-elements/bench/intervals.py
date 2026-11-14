# LeetCode #2121: Intervals Between Identical Elements -- the benchmark,
# the same algorithm as intervals.kara: each value's indices gathered in
# a dict, then one running sum per list.


def get_distances(arr):
    positions = {}
    for i in range(len(arr)):
        positions.setdefault(arr[i], []).append(i)
    answer = [0] * len(arr)
    for p in positions.values():
        c = len(p)
        total = sum(p)
        before = 0
        for k in range(c):
            pk = p[k]
            after = total - before - pk
            answer[pk] = k * pk - before + after - (c - k - 1) * pk
            before += pk
    return answer


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    seed = [2121]
    arrays = []
    for g in range(40):
        top = [10, 100, 1000, 10000][g % 4]
        arrays.append([next_random(seed) % top + 1 for _ in range(50000)])
    total = 0
    check = 0
    for rnd in range(20):
        for g in range(40):
            arrays[g][(rnd * 7919 + g * 104729) % 50000] += 1
            s = sum(get_distances(arrays[g]))
            total += s
            check = (check * 31 + s % 1000000007) % 1000000007
    print(f"800 solves: distances sum to {total}, checksum {check}")


main()
