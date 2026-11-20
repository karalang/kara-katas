# LeetCode #1238: the benchmark, mirroring the Kāra file.


def circular_permutation(n, start):
    return [start ^ i ^ (i >> 1) for i in range(1 << n)]


def is_cycle(n, start, p):
    size = 1 << n
    if len(p) != size or p[0] != start:
        return False
    seen = [False] * size
    for v in p:
        if v < 0 or v >= size or seen[v]:
            return False
        seen[v] = True
    for i in range(size):
        d = p[i] ^ p[(i + 1) % size]
        if d == 0 or d & (d - 1) != 0:
            return False
    return True


cycles = 0
check = 0
for k in range(64):
    start = (k * 1031) % 65536
    p = circular_permutation(16, start)
    if is_cycle(16, start, p):
        cycles += 1
    check = (check * 131 + p[32768]) % 1000000007
print(f"n = 16, 64 starts: {cycles} cycles, checksum {check}")
