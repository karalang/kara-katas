# Benchmark for #403: mirror of frog_jump.kara (the jump sizes that reach
# each stone).


def can_cross(stones):
    jumps = {s: set() for s in stones}
    jumps[stones[0]].add(0)
    for s in stones:
        for k in list(jumps[s]):
            for size in (k - 1, k, k + 1):
                if size > 0 and s + size in jumps:
                    jumps[s + size].add(size)
    return len(jumps[stones[-1]]) > 0


def main():
    rivers = 600
    n = 2000
    seed = 403
    crossed = 0
    checksum = 0
    for r in range(rivers):
        stones = [0, 1]
        while len(stones) < n:
            seed = (seed * 1103515245 + 12345) % 2147483648
            stones.append(stones[-1] + 1 + seed // 65536 % 3)
        if can_cross(stones):
            crossed += 1
            checksum = (checksum * 31 + r + 1) % 1000000007
    print(f"{rivers} rivers of {n} stones: {crossed} crossed, checksum {checksum}")


main()
