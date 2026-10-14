# Benchmark for #594: Python mirror of the ★ arm (count in a dict, then
# pair); see find_lhs.kara.


def find_lhs(nums):
    count = {}
    for x in nums:
        count[x] = count.get(x, 0) + 1
    best = 0
    for v, c in count.items():
        d = count.get(v + 1)
        if d is not None:
            best = max(best, c + d)
    return best


# ---- benchmark ---------------------------------------------------------------

def step(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def wide(seed):
    hi = step(seed)
    lo = step(seed)
    return hi * 32768 + lo


def main():
    count = 100
    rounds = 20
    seed = [594]
    arrays = []
    for _ in range(count):
        rng = 1 + wide(seed) % 5000
        low = wide(seed) % 1999990000 - 999990000
        arrays.append([low + wide(seed) % rng for _ in range(20000)])
    total = 0
    checksum = 0
    for rnd in range(rounds):
        for g in range(count):
            got = find_lhs(arrays[(rnd * 7 + g) % count])
            total += got
            checksum = (checksum * 31 + got) % 1000000007
    print(f"{count} arrays, {rounds} rounds: total {total}, checksum {checksum}")


main()
