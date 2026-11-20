# LeetCode #2263: Make Array Non-decreasing or Non-increasing -- Python
# mirror of the ★ arm (convert.kara) on the bench workload: the slope
# trick with a max-heap (heapq of negatives), forwards and over the
# reversed array, the smaller cost. Output is byte-identical to
# convert.kara.
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


# ---- bench harness ---------------------------------------------------------

seed = 2263


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    check = 0
    for _ in range(400):
        nums = [next_random() % 1001 for _ in range(1000)]
        check = (check * 31 + convert_array(nums)) % 1000000007
    print(f"400 arrays of 1000: checksum {check}")


main()
