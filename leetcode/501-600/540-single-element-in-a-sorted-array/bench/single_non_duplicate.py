# Benchmark for #540: Python mirror of the ★ arm (binary search over the
# pairs); see single_non_duplicate.kara.


def single_non_duplicate(nums):
    low, high = 0, len(nums) - 1
    while low < high:
        mid = (low + high) // 2
        if mid % 2 == 1:
            mid -= 1
        if nums[mid] == nums[mid + 1]:
            low = mid + 2
        else:
            high = mid
    return nums[low]


seed = 540


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # 100 arrays of 0 to 49,999 pairs and the single element at a
    # random place, values rising by 1 or 2, built once. Then the answer
    # for each array is found 200,000 times.
    arrays = 100
    all_arrays = []
    elements = 0
    for _ in range(arrays):
        high = next_random()
        pairs = (high * 32768 + next_random()) % 50000
        high = next_random()
        single = (high * 32768 + next_random()) % (pairs + 1)
        nums = []
        v = 0
        for i in range(pairs + 1):
            v += 1 + next_random() % 2
            nums.append(v)
            if i != single:
                nums.append(v)
        elements += len(nums)
        all_arrays.append(nums)
    total = 0
    checksum = 0
    for _ in range(200000):
        for nums in all_arrays:
            answer = single_non_duplicate(nums)
            total += answer
            checksum = (checksum * 31 + answer) % 1000000007
    print(f"{arrays} arrays, {elements} elements, 200000 times each: total {total}, checksum {checksum}")


main()
