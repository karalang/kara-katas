# LeetCode #2439: Minimize Maximum of Array -- the bench, the ★ arm: the
# largest ceiling average of any prefix, in one pass.


def minimize_array_value(nums):
    total = 0
    answer = 0
    for i in range(len(nums)):
        total += nums[i]
        answer = max(answer, (total + i) // (i + 1))
    return answer


seed = 2439


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return (a * 32768 + next_random()) % 1000000001


def main():
    arrays = [[wide() for _ in range(100000)] for _ in range(10)]
    check = 0
    for p in range(100):
        for c in range(len(arrays)):
            at = (p * 7919 + c * 104729) % 100000
            arrays[c][at] = wide()
            check = (check * 31 + minimize_array_value(arrays[c]) + p) % 1000000007
    print(f"100 passes over 10 arrays of 10^5 values: checksum {check}")


main()
