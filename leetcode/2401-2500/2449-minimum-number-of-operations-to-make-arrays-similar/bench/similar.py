# LeetCode #2449: Minimum Number of Operations to Make Arrays Similar --
# the bench, the ★ arm: the odd and the even values of each array sorted
# and matched in order, the distance over 4.


def make_similar(nums, target):
    odd = []
    even = []
    for x in nums:
        if x % 2 == 1:
            odd.append(x)
        else:
            even.append(x)
    odd_target = []
    even_target = []
    for x in target:
        if x % 2 == 1:
            odd_target.append(x)
        else:
            even_target.append(x)
    odd.sort()
    even.sort()
    odd_target.sort()
    even_target.sort()
    distance = 0
    for i in range(len(odd)):
        distance += abs(odd[i] - odd_target[i])
    for i in range(len(even)):
        distance += abs(even[i] - even_target[i])
    return distance // 4


seed = 2449


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    r = next_random()
    return r * 32768 + next_random()


def main():
    n = 100000
    nums = [1 + wide_random() % 1000000 for _ in range(n)]
    target = list(nums)
    check = 0
    for p in range(220):
        for _ in range(1000):
            i = wide_random() % n
            j = wide_random() % n
            step = 2 * (1 + next_random() % 50)
            if i != j and target[i] + step <= 1000000 and target[j] - step >= 1:
                target[i] += step
                target[j] -= step
        check = (check * 31 + make_similar(nums, target) + p) % 1000000007
    print(f"220 passes over 10^5 values: checksum {check}")


main()
