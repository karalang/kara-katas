# LeetCode #2772: Apply Operations to Make All Array Elements Equal to
# Zero -- the bench in Python: the ★ arm over 20 arrays of 10^5 numbers,
# all drawn first, then each answered 40 times.


def check_array(nums, k):
    n = len(nums)
    ends = [0] * (n + 1)
    covering = 0
    for i in range(n):
        covering -= ends[i]
        left = nums[i] - covering
        if left < 0:
            return False
        if left > 0:
            if i + k > n:
                return False
            covering += left
            ends[i + k] += left
    return True


seed = 2772


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def built(n, k, most):
    nums = [0] * n
    ops = [0] * n
    running = 0
    for i in range(n):
        if i + k <= n:
            ops[i] = next_random() % (most + 1)
        running += ops[i]
        if i >= k:
            running -= ops[i - k]
        nums[i] = running
    if next_random() % 2 == 1:
        at = wide() % n
        if nums[at] > 0 and next_random() % 2 == 1:
            nums[at] -= 1
        else:
            nums[at] += 1
    return nums


def main():
    count = 20
    rounds = 40
    cases = []
    for _ in range(count):
        k = wide() % 1000 + 1
        cases.append((built(100000, k, 9), k))
    yes = 0
    check = 0
    for r in range(rounds):
        for nums, k in cases:
            a = check_array(nums, k)
            yes += a
            check = (check * 31 + (2 if a else 1) + r) % 1000000007
    print(f"{count} arrays of 10^5, {rounds} rounds: {yes} true, checksum {check}")


main()
