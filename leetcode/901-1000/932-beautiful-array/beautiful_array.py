# LeetCode #932: Beautiful Array -- divide and conquer with a memo
# (Python mirror).


def build(n, memo):
    if n in memo:
        return list(memo[n])
    out = []
    if n == 1:
        out.append(1)
    else:
        for x in build((n + 1) // 2, memo):
            out.append(2 * x - 1)
        for x in build(n // 2, memo):
            out.append(2 * x)
    memo[n] = list(out)
    return out


def beautiful_array(n):
    return build(n, {})


# ---- test harness ---------------------------------------------------------


def beautiful(nums, n):
    if len(nums) != n:
        return False
    pos = [-1] * (n + 1)
    for i in range(n):
        v = nums[i]
        if v < 1 or v > n or pos[v] >= 0:
            return False
        pos[v] = i
    for k in range(n):
        for i in range(k):
            v = 2 * nums[k] - nums[i]
            if 1 <= v <= n and pos[v] > k:
                return False
    return True


def listed(nums):
    return ", ".join(str(x) for x in nums)


def show(name, n):
    nums = beautiful_array(n)
    verdict = "beautiful" if beautiful(list(nums), n) else "NOT beautiful"
    print(f"{name}: [{listed(nums)}], {verdict}")


def main():
    show("example 1 (n = 4)", 4)
    show("example 2 (n = 5)", 5)
    show("n = 1", 1)
    show("n = 2", 2)
    show("n = 3", 3)
    show("n = 8", 8)
    show("n = 9", 9)
    bad = 0
    for n in range(1, 101):
        if not beautiful(beautiful_array(n), n):
            bad += 1
    print(f"n from 1 to 100: {100 - bad} beautiful, {bad} not")
    elements = 0
    check = 0
    for n in range(1, 1001):
        for x in beautiful_array(n):
            elements += 1
            check = (check * 1000003 + x) % 1000000007
    print(f"n from 1 to 1000: {elements} elements, checksum {check}")
    big = beautiful_array(1000)
    verdict = "beautiful" if beautiful(list(big), 1000) else "NOT beautiful"
    print(f"n = 1000: {verdict}, starting {big[0]}, {big[1]}, {big[2]}, {big[3]} and ending {big[996]}, {big[997]}, {big[998]}, {big[999]}")


main()
