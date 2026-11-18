# LeetCode #1199: Minimum Time to Build Blocks -- the ★ arm in Python:
# Huffman's merge on a smallest-first heap, the two quickest blocks merged
# into one taking split more than the slower, until one is left.
import heapq


def min_build_time(blocks, split):
    heap = list(blocks)
    heapq.heapify(heap)
    while len(heap) > 1:
        heapq.heappop(heap)
        slower = heapq.heappop(heap)
        heapq.heappush(heap, slower + split)
    return heap[0]


# ---- test harness ---------------------------------------------------------

seed = 1199


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(v):
    return "[" + ", ".join(map(str, v)) + "]"


def main():
    cases = [([1], 1), ([1, 2], 5), ([1, 2, 3], 1), ([5, 5, 5, 5], 2), ([1, 1, 1, 100], 10), ([10, 1, 1, 1, 1], 3)]
    for blocks, split in cases:
        print(f"{show(blocks)}, split {split}: {min_build_time(blocks, split)}")
    print(f"1000 blocks of 1, split 100: {min_build_time([1] * 1000, 100)}")
    print(f"1000 blocks of 100000, split 100: {min_build_time([100000] * 1000, 100)}")
    print(f"512 blocks of 7, split 1: {min_build_time([7] * 512, 1)}")
    print(f"1000 blocks of 7, split 1: {min_build_time([7] * 1000, 1)}")
    print(f"513 blocks of 7, split 1: {min_build_time([7] * 513, 1)}")
    total = 0
    check = 0
    for _ in range(1000):
        n = next_random() % 12 + 1
        split = next_random() % 20 + 1
        blocks = [next_random() % 50 + 1 for _ in range(n)]
        t = min_build_time(blocks, split)
        total += t
        check = (check * 131 + t) % 1000000007
    print(f"1000 random block sets: total {total}, checksum {check}")
    big = []
    for _ in range(1000):
        high = next_random()
        low = next_random()
        big.append((high * 32768 + low) % 100000 + 1)
    print(f"1000 random blocks up to 100000, split 100: {min_build_time(big, 100)}")
    print(f"the same, split 1: {min_build_time(big, 1)}")


main()
