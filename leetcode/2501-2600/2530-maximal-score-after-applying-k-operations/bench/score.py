# LeetCode #2530: Maximal Score After Applying K Operations -- benchmark
# mirror of the ★ arm (score.kara): 10^5 numbers built once, then the
# passes, each asking for the score with a `k` the checksum picks.
import heapq


def max_kelements(nums, k):
    heap = [-x for x in nums]
    heapq.heapify(heap)
    score = 0
    for _ in range(k):
        top = -heapq.heappop(heap)
        score += top
        heapq.heappush(heap, -((top + 2) // 3))
    return score


seed = 2530


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    return next_random() * 32768 + next_random()


def main():
    nums = [wide_random() % 1000000000 + 1 for _ in range(100000)]
    passes = 170
    check = 0
    for p in range(passes):
        k = 50000 + check % 50001
        check = (check * 31 + max_kelements(nums, k) % 1000000007 + p) % 1000000007
    print(f"{passes} passes over 100000 numbers: checksum {check}")


main()
