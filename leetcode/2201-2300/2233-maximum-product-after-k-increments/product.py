# LeetCode #2233: Maximum Product After K Increments -- the mirror of
# product.kara: each increment to the smallest number, through a heap,
# and the product modulo 10^9 + 7.
import heapq


def maximum_product(nums, k):
    queue = list(nums)
    heapq.heapify(queue)
    for _ in range(k):
        heapq.heappush(queue, heapq.heappop(queue) + 1)
    product = 1
    for x in queue:
        product = product * x % 1000000007
    return product


seed = 2233


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    high = next_random()
    return high * 32768 + next_random()


def show(nums, k):
    print(f"[{', '.join(str(x) for x in nums)}], k = {k} -> {maximum_product(nums, k)}")


def main():
    show([0, 4], 5)
    show([6, 3, 3, 2], 2)
    show([0], 1)
    show([0, 0], 1)
    show([1, 2, 3, 4], 10)
    show([1000000, 999999, 999998], 3)
    show([5, 5, 5], 4)
    check = 0
    for c in range(3000):
        n = next_random() % 20 + 1
        top = [10, 1000, 1000000][c % 3]
        nums = [wide_random() % (top + 1) for _ in range(n)]
        k = next_random() % 100 + 1
        check = (check * 31 + maximum_product(nums, k)) % 1000000007
    print(f"3000 cases: checksum {check}")
    for top in [1000000, 10]:
        nums = [wide_random() % (top + 1) for _ in range(100000)]
        print(f"10^5 numbers of up to {top}, k = 10^5: {maximum_product(nums, 100000)}")


main()
