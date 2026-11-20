# LeetCode #1708: Largest Subarray Length K -- the Python mirror of the ★
# arm (largest.kara): the largest first value among the starts that leave
# room for k.


def largest_subarray(nums, k):
    best = 0
    for i in range(1, len(nums) - k + 1):
        if nums[i] > nums[best]:
            best = i
    return nums[best:best + k]


def next_random(state):
    state[0] = (state[0] * 1103515245 + 12345) % 2147483648
    return state[0] // 65536


def batch(count, most, seed):
    firsts = 0
    check = 0
    for _ in range(count):
        n = next_random(seed) % most + 1
        nums = list(range(1, n + 1))
        for i in range(n - 1, 0, -1):
            j = next_random(seed) % (i + 1)
            nums[i], nums[j] = nums[j], nums[i]
        for i in range(n):
            nums[i] = nums[i] * 10 + next_random(seed) % 10
        k = next_random(seed) % n + 1
        answer = largest_subarray(nums, k)
        firsts += answer[0]
        for v in answer:
            check = (check * 31 + v) % 1000000007
        check = (check * 31 + k) % 1000000007
    print(f"{count} arrays of up to {most} values: first values sum to {firsts}, checksum {check}")


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    # LeetCode's three examples, then all of it and the largest last
    print(show(largest_subarray([1, 4, 5, 2, 3], 3)))
    print(show(largest_subarray([1, 4, 5, 2, 3], 4)))
    print(show(largest_subarray([1, 4, 5, 2, 3], 1)))
    print(show(largest_subarray([3, 1, 2], 3)))
    print(show(largest_subarray([1, 2, 9], 2)))
    seed = [1708]
    batch(3000, 10, seed)
    batch(300, 1000, seed)
    batch(10, 100000, seed)


main()
