# LeetCode #2411: Smallest Subarrays With Maximum Bitwise OR -- the bench,
# the ★ arm in Python: walking from the right, the nearest index holding
# each of the 30 bits, the subarray from i reaching the farthest of them.

seed = 2411


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def smallest_subarrays(nums):
    n = len(nums)
    nearest = [-1] * 30
    answer = [1] * n
    for i in range(n - 1, -1, -1):
        reach = i
        for bit in range(30):
            if nums[i] >> bit & 1:
                nearest[bit] = i
            reach = max(reach, nearest[bit])
        answer[i] = reach - i + 1
    return answer


def main():
    arrays = [[(next_random() * 32768 + next_random()) % (1 << (6 * i + 6)) for _ in range(100000)] for i in range(5)]
    check = 0
    for p in range(10):
        for nums in arrays:
            for a in smallest_subarrays(nums):
                check = (check * 31 + a + p) % 1000000007
    print(f"10 passes over 5 arrays of 10^5 values: checksum {check}")


main()
