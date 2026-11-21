# LeetCode #2419: Longest Subarray With Maximum Bitwise AND -- mirror of
# the ★ arm: one scan keeping the largest value so far and the run of it
# ending here.

seed = 2419


def longest_subarray(nums):
    top = run = best = 0
    for x in nums:
        if x > top:
            top, run, best = x, 0, 0
        if x == top:
            run += 1
            best = max(best, run)
        else:
            run = 0
    return best


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def values(n, top, stay):
    nums = []
    for i in range(n):
        if i > 0 and next_random() % stay == 0:
            nums.append(nums[i - 1])
        else:
            a = next_random()
            nums.append(1 + (a * 32768 + next_random()) % top)
    return nums


def main():
    for nums in ([1, 2, 3, 3, 2, 2], [1, 2, 3, 4], [1000000], [7, 7, 7, 7, 7],
                 [9, 9, 1, 9, 9, 9, 2, 9], [6, 5, 3, 6, 6, 1, 6, 6]):
        print(longest_subarray(nums))
    print(longest_subarray(values(100000, 1000000, 2)))
    print(longest_subarray(values(100000, 3, 50)))
    check = total = 0
    for _ in range(3000):
        n = 1 + next_random() % 30
        top = 1 + next_random() % 8
        a = longest_subarray(values(n, top, 1 + next_random() % 4))
        total += a
        check = (check * 31 + a) % 1000000007
    print(f"3000 random: checksum {check}, total {total}")


if __name__ == "__main__":
    main()
