# LeetCode #2149: Rearrange Array Elements by Sign -- the benchmark's
# Python mirror of signs.kara.


def rearrange_array(nums):
    out = [0] * len(nums)
    positive = 0
    negative = 1
    for x in nums:
        if x > 0:
            out[positive] = x
            positive += 2
        else:
            out[negative] = x
            negative += 2
    return out


seed = 2149


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    hi = next_random()
    return hi * 32768 + next_random()


def main():
    n = 200000
    lists = []
    for _ in range(4):
        nums = []
        for i in range(n):
            size = next_random() % 100000 + 1
            nums.append(size if i < n // 2 else -size)
        for i in range(n - 1, 0, -1):
            j = wide() % (i + 1)
            nums[i], nums[j] = nums[j], nums[i]
        lists.append(nums)
    check = 0
    for rnd in range(25):
        for l in range(4):
            a = wide() % n
            b = wide() % n
            lists[l][a], lists[l][b] = lists[l][b], lists[l][a]
            out = rearrange_array(lists[l])
            at = wide() % n
            check = (check * 31 + out[0] + out[n - 1] + out[at] + 300000 + rnd) % 1000000007
    print(f"100 answers: checksum {check}")


main()
