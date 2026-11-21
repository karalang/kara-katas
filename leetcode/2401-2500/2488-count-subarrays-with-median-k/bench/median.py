# LeetCode #2488: Count Subarrays With Median K -- Python mirror of the ★
# arm's benchmark (median.kara): the same 20 orders and passes, the
# balances of the starts counted in a dict.


def count_subarrays(nums, k):
    n = len(nums)
    at = nums.index(k)
    starts = {0: 1}
    balance = 0
    for i in range(at - 1, -1, -1):
        balance += 1 if nums[i] > k else -1
        starts[balance] = starts.get(balance, 0) + 1
    count = 0
    balance = 0
    for j in range(at, n):
        if j > at:
            balance += 1 if nums[j] > k else -1
        count += starts.get(-balance, 0) + starts.get(1 - balance, 0)
    return count


seed = 2488


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    n = 10000
    passes = 400
    orders = []
    for _ in range(20):
        nums = list(range(1, n + 1))
        for i in range(n - 1, 0, -1):
            j = next_random() % (i + 1)
            nums[i], nums[j] = nums[j], nums[i]
        orders.append(nums)
    check = 0
    for p in range(passes):
        for o in range(20):
            nums = orders[o]
            a, b = check % n, (check // n + p) % n
            nums[a], nums[b] = nums[b], nums[a]
            k = (check + o) % n + 1
            check = (check * 31 + count_subarrays(nums, k) + p) % 1000000007
    print(f"{passes} passes over 20 orders of 10^4: checksum {check}")


main()
