# Benchmark for #362 -- mirror of hit_counter.kara.
from collections import deque


def main():
    hits = deque()
    seed = 362
    t = 1
    checksum = 0
    for _ in range(2000000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        t += (seed // 65536) % 3
        seed = (seed * 1103515245 + 12345) % 2147483648
        if (seed // 65536) % 4 == 0:
            while hits and hits[0] <= t - 300:
                hits.popleft()
            checksum = (checksum * 31 + len(hits)) % 1000000007
        else:
            hits.append(t)
    print(f"checksum {checksum}")


main()
