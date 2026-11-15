# benchmark's Python mirror of pairs.kara (LeetCode #2206, the ★ arm): a
# count per value up to 500, then one pass over the counts.


def divide_array(nums):
    count = [0] * 501
    for x in nums:
        count[x] += 1
    for c in count:
        if c % 2 == 1:
            return False
    return True


seed = 2206


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


# 1000 numbers up to `top`: 500 pairs shuffled, or 1000 drawn freely
def random_array(paired, top):
    nums = []
    if paired:
        for _ in range(500):
            x = next_random() % top + 1
            nums.append(x)
            nums.append(x)
        for i in range(999, 0, -1):
            j = next_random() % (i + 1)
            nums[i], nums[j] = nums[j], nums[i]
    else:
        for _ in range(1000):
            nums.append(next_random() % top + 1)
    return nums


def main():
    arrays = [random_array(a % 4 != 3, [2, 5, 500][a % 3]) for a in range(200)]
    # each odd pass punches one number of every array before the count and
    # puts it back after
    check = 0
    for p in range(1500):
        for a in range(200):
            at = (p * 7 + a) % 1000
            old = arrays[a][at]
            if p % 2 == 1:
                arrays[a][at] = (p + a) % 500 + 1
            paired = divide_array(arrays[a])
            arrays[a][at] = old
            check = (check * 31 + (2 if paired else 1)) % 1000000007
    print(f"1500 passes over 200 arrays: checksum {check}")


main()
