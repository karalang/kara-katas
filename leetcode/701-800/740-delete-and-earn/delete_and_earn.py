# LeetCode #740: Delete and Earn -- house robber over values.
# Mirror of the Kara star arm: total the points each value is worth,
# then walk the values in order keeping the best total with the last
# value taken and with it left.


def delete_and_earn(nums):
    top = 0
    for x in nums:
        if x > top:
            top = x
    points = [0] * (top + 1)
    for x in nums:
        points[x] += x
    take = 0
    skip = 0
    for v in range(top + 1):
        taken = skip + points[v]
        skip = take if take > skip else skip
        take = taken
    return take if take > skip else skip


# ---- test harness ---------------------------------------------------------

def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def show(nums):
    print(f"[{', '.join(str(x) for x in nums)}] -> {delete_and_earn(nums)}")


def main():
    show([3, 4, 2])
    show([2, 2, 3, 3, 3, 4])
    show([1])
    show([5, 5, 5, 5])
    show([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    show([10, 1, 9, 2, 8, 3])
    show([1, 1, 1, 2, 4, 5, 5, 5, 6])
    show([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 9, 7, 9])
    seed = [740]
    random = [1 + next_random(seed) % 10000 for _ in range(20000)]
    print(f"20000 random numbers up to 10000 -> {delete_and_earn(random)}")
    every = list(range(1, 10001))
    print(f"every number from 1 to 10000 once -> {delete_and_earn(every)}")
    crowded = [1 + next_random(seed) % 50 for _ in range(20000)]
    print(f"20000 random numbers up to 50 -> {delete_and_earn(crowded)}")
    total = 0
    most = 0
    for _ in range(300):
        n = 1 + next_random(seed) % 12
        rng = 1 + next_random(seed) % 10
        nums = [1 + next_random(seed) % rng for _ in range(n)]
        got = delete_and_earn(nums)
        most += got
        total = (total * 131 + got + 1) % 1000000007
    print(f"300 random short lists: {most} points in all, checksum {total}")


main()
