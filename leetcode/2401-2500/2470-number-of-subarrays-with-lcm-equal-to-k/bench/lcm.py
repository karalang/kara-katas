# LeetCode #2470: Number of Subarrays With LCM Equal to K -- the bench,
# the ★ arm in Python: from each start the running LCM, the walk stopped
# once it no longer divides `k`.


def gcd(a, b):
    return a if b == 0 else gcd(b, a % b)


def subarray_lcm(nums, k):
    n = len(nums)
    count = 0
    for start in range(n):
        lcm = 1
        for end in range(start, n):
            lcm = lcm // gcd(lcm, nums[end]) * nums[end]
            if k % lcm != 0:
                break
            if lcm == k:
                count += 1
    return count


seed = 2470


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # 10 lists of 1000 numbers built once, each a random divisor of 720
    # but one in 50 any number from 1 to 1000; then 90 passes, each
    # setting one number of every list from the checksum so far, then
    # answering it with `k` 720 and folding the count plus the pass into
    # the checksum
    divisors = [d for d in range(1, 721) if 720 % d == 0]
    lists = []
    for _ in range(10):
        nums = []
        for _ in range(1000):
            if next_random() % 50 == 0:
                nums.append(1 + next_random() % 1000)
            else:
                nums.append(divisors[next_random() % len(divisors)])
        lists.append(nums)
    check = 0
    for p in range(90):
        for a in range(len(lists)):
            lists[a][(check + a) % 1000] = divisors[check % len(divisors)]
            check = (check * 31 + subarray_lcm(lists[a], 720) + p) % 1000000007
    print(f"90 passes over 10 lists of 1000: checksum {check}")


main()
