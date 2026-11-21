# LeetCode #2454: Next Greater Element IV -- bench, Python mirror of
# second.kara: two monotonic stacks, the first waiting for one greater
# value and the second for another.


def second_greater_element(nums):
    n = len(nums)
    answer = [-1] * n
    first = []
    second = []
    for j in range(n):
        while len(second) > 0 and nums[second[-1]] < nums[j]:
            answer[second.pop()] = nums[j]
        cut = len(first)
        while cut > 0 and nums[first[cut - 1]] < nums[j]:
            cut -= 1
        for i in range(cut, len(first)):
            second.append(first[i])
        del first[cut:]
        first.append(j)
    return answer


seed = 2454


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    n = 100000
    arrays = []
    for _ in range(10):
        nums = []
        for _ in range(n):
            hi = next_random()
            nums.append((hi * 32768 + next_random()) % 1000000001)
        arrays.append(nums)
    check = 0
    for p in range(20):
        for a in range(10):
            arrays[a][(p * 7919 + a) % n] = check % 1000000001
            for v in second_greater_element(arrays[a]):
                check = (check * 31 + v + 1) % 1000000007
            check = (check + p) % 1000000007
    print(f"20 passes over 10 arrays of 10^5 values: checksum {check}")


main()
