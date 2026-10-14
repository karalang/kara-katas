# LeetCode #632: Smallest Range Covering Elements from K Lists -- Python
# mirror of the ★ arm.
#
# One value from each list in a smallest-first heap, the largest of them
# tracked beside it; the smallest is replaced by the next value of its
# list until a list runs out.
import heapq


def smallest_range(nums):
    queue = []
    high = nums[0][0]
    for lst in range(len(nums)):
        heapq.heappush(queue, (nums[lst][0], lst, 0))
        high = max(high, nums[lst][0])
    best_low = best_high = 0
    found = False
    while True:
        low, lst, at = heapq.heappop(queue)
        if not found or high - low < best_high - best_low:
            best_low, best_high, found = low, high, True
        if at + 1 == len(nums[lst]):
            break
        nxt = nums[lst][at + 1]
        high = max(high, nxt)
        heapq.heappush(queue, (nxt, lst, at + 1))
    return [best_low, best_high]


seed = 632


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_lists(count, shortest, longest, least, most):
    nums = []
    for _ in range(count):
        lst = []
        for _ in range(shortest + next_random() % (longest - shortest + 1)):
            wide = next_random() * 32768 + next_random()
            lst.append(least + wide % (most - least + 1))
        lst.sort()
        nums.append(lst)
    return nums


def show(nums):
    text = ", ".join("[" + ",".join(str(v) for v in lst) + "]" for lst in nums)
    r = smallest_range(nums)
    print(f"[{text}] -> [{r[0]}, {r[1]}]")


show([[4, 10, 15, 24, 26], [0, 9, 12, 20], [5, 18, 22, 30]])
show([[1, 2, 3], [1, 2, 3], [1, 2, 3]])
show([[5]])
show([[1, 9], [4, 6]])
show([[-100000, 100000], [0]])
show([[1, 1, 1], [1]])
show([[10], [40], [20], [30]])
show([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [-5, 10], [10, 20, 30]])
total = checksum = 0
for _ in range(300):
    count = 1 + next_random() % 8
    r = smallest_range(random_lists(count, 1, 10, -50, 50))
    total += r[1] - r[0]
    checksum = (checksum * 31 + r[0] * 101 + r[1] + 1000000) % 1000000007
print(f"300 random cases: total width {total}, checksum {checksum}")
r = smallest_range(random_lists(100, 50, 50, -100000, 100000))
print(f"100 lists of 50 values -> [{r[0]}, {r[1]}]")
