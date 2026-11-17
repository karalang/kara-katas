# LeetCode #2233: Maximum Product After K Increments -- the benchmark's
# Python mirror of product.kara: the smallest raised k times through a
# min-heap (heapq), then the heap emptied into the product.
import heapq


def maximum_product(nums, k):
    queue = []
    for x in nums:
        heapq.heappush(queue, x)
    for _ in range(k):
        smallest = heapq.heappop(queue)
        heapq.heappush(queue, smallest + 1)
    product = 1
    while queue:
        product = product * heapq.heappop(queue) % 1000000007
    return product


seed = 2233


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    high = next_random()
    return high * 32768 + next_random()


def main():
    nums = [wide_random() % 1000001 for _ in range(20000)]
    check = 0
    for _ in range(150):
        # punch: one number drawn again before each pass
        at = next_random() % 20000
        nums[at] = wide_random() % 1000001
        check = (check * 31 + maximum_product(nums, 50000)) % 1000000007
    print(f"150 passes over 20000 numbers, k = 50000: checksum {check}")


main()
