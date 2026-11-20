# LeetCode #2263: Make Array Non-decreasing or Non-increasing -- Python
# mirror of the ★ arm (convert.kara): the slope trick with a max-heap
# (heapq of negatives), once forwards and once over the reversed array,
# the smaller cost. Output is byte-identical to convert.kara.
import heapq


def nondecreasing_cost(nums):
    heap = []
    cost = 0
    for x in nums:
        heapq.heappush(heap, -x)
        if -heap[0] > x:
            cost += -heapq.heappop(heap) - x
            heapq.heappush(heap, -x)
    return cost


def convert_array(nums):
    return min(nondecreasing_cost(nums), nondecreasing_cost(nums[::-1]))


# ---- test harness ---------------------------------------------------------

seed = 2263


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    examples = [
        [3, 2, 4, 5, 0],
        [2, 2, 3, 4],
        [0],
        [5, 4, 3, 2, 1],
        [1, 3, 2],
        [0, 1000, 0, 1000, 0],
        [9, 4, 1, 0, 1, 4, 9],
    ]
    for nums in examples:
        print(f"{show(nums)} -> {convert_array(list(nums))}")
    check = 0
    for t in range(2000):
        n = next_random() % 30 + 1
        top = [3, 10, 100, 1000][t % 4]
        nums = [next_random() % (top + 1) for _ in range(n)]
        check = (check * 31 + convert_array(nums)) % 1000000007
    print(f"2000 arrays: checksum {check}")
    rand = [next_random() % 1001 for _ in range(1000)]
    zigzag = [(i % 2) * 1000 for i in range(1000)]
    spiked = [1000 if i % 10 == 9 else 1000 - i for i in range(1000)]
    print(f"1000 values: {show([convert_array(rand), convert_array(zigzag), convert_array(spiked)])}")


main()
