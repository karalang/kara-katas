# LeetCode #1199 bench: the ★ arm in Python, over the same 200 sets of 1000
# blocks and 50 rounds as the Kāra bench.
import heapq


def min_build_time(blocks, split):
    heap = list(blocks)
    heapq.heapify(heap)
    while len(heap) > 1:
        heapq.heappop(heap)
        slower = heapq.heappop(heap)
        heapq.heappush(heap, slower + split)
    return heap[0]


def main():
    seed = 1199

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    highs = [10, 1000, 100000]
    sets = []
    for k in range(200):
        high = highs[k % 3]
        split = next_random() % 100 + 1
        blocks = []
        for _ in range(1000):
            a = next_random()
            b = next_random()
            blocks.append((a * 32768 + b) % high + 1)
        sets.append((blocks, split))
    check = 0
    for _ in range(50):
        for blocks, split in sets:
            t = min_build_time(blocks, split)
            check = (check * 131 + t) % 1000000007
    print(f"50 rounds of 200 sets of 1000 blocks: checksum {check}")


main()
