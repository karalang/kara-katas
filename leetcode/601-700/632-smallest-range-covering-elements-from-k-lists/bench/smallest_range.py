# LeetCode 632 -- Smallest Range Covering Elements from K Lists, bench
# mirror in Python.
#
# The ★ arm of smallest_range.kara: one value from each list in a
# smallest-first `heapq` of (value, list, index) triples, with the
# largest held value tracked beside it. Same 10 inputs, same 30 rounds,
# same output line.
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


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def random_lists(count, length, seed):
    nums = []
    for _ in range(count):
        lst = []
        for _ in range(length):
            wide = next_random(seed) * 32768 + next_random(seed)
            lst.append(wide % 200001 - 100000)
        lst.sort()
        nums.append(lst)
    return nums


def main():
    seed = [632]
    inputs = [random_lists(3500, 50, seed) for _ in range(10)]
    rounds = 30
    total = checksum = 0
    for rnd in range(rounds):
        r = smallest_range(inputs[rnd % 10])
        total += r[1] - r[0]
        checksum = (checksum * 31 + r[0] * 101 + r[1] + 100000000) % 1000000007
    print(f"10 inputs of 3500 lists, {rounds} rounds: total width {total}, checksum {checksum}")


main()
