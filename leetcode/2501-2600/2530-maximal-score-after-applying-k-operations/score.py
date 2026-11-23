# LeetCode #2530: Maximal Score After Applying K Operations -- Python
# mirror of the ★ arm (score.kara): a max-heap (heapq over negated
# numbers), `k` times the largest popped, added, and its third rounded up
# pushed back.
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


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def wide_random(seed):
    return next_random(seed) * 32768 + next_random(seed)


def show(xs):
    return "[" + ", ".join(str(x) for x in xs) + "]"


def main():
    fixed = [
        ([10, 10, 10, 10, 10], 5),
        ([1, 10, 3, 3, 3], 3),
        ([1], 1),
        ([1], 100000),
        ([1000000000], 25),
        ([2, 2], 3),
        ([9, 3, 1], 4),
        ([7, 7, 7], 7),
    ]
    for nums, k in fixed:
        print(f"{show(nums)} k {k} -> {max_kelements(nums, k)}")
    seed = [2530]
    for count, most, top, ops in [(2000, 20, 30, 30), (200, 1000, 1000000000, 2000)]:
        total = 0
        check = 0
        for _ in range(count):
            n = next_random(seed) % most + 1
            nums = [wide_random(seed) % top + 1 for _ in range(n)]
            k = next_random(seed) % ops + 1
            a = max_kelements(nums, k)
            total += a
            check = (check * 31 + a % 1000000007) % 1000000007
        print(f"{count} random lists of up to {most} numbers to {top}: total {total}, checksum {check}")
    nums = [wide_random(seed) % 1000000000 + 1 for _ in range(100000)]
    print(f"10^5 numbers, k 10^5: {max_kelements(nums, 100000)}")


main()
