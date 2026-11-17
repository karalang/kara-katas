# LeetCode #2216: Minimum Deletions to Make Array Beautiful -- the mirror
# of beautiful.kara: a number that would start a pair is deleted when the
# number after it is the same; an odd length left costs one more.


def min_deletion(nums):
    n = len(nums)
    deleted = 0
    for i in range(n - 1):
        if (i - deleted) % 2 == 0 and nums[i] == nums[i + 1]:
            deleted += 1
    if (n - deleted) % 2 == 1:
        deleted += 1
    return deleted


seed = 2216


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


# a draw of 30 bits, since one draw stops at 32767
def wide_random():
    return next_random() * 32768 + next_random()


def random_nums(n, top):
    return [wide_random() % (top + 1) for _ in range(n)]


def show(nums):
    print(f"{nums} -> {min_deletion(nums)}")


def main():
    # LeetCode's two examples, then four more: one number, two alike,
    # already beautiful, and one value throughout
    show([1, 1, 2, 3, 5])
    show([1, 1, 2, 2, 3, 3])
    show([7])
    show([4, 4])
    show([1, 2, 1, 2])
    show([9, 9, 9, 9, 9])
    # 3000 random arrays of 1 to 30 numbers up to 1, 3 and 10^5 in turn
    check = 0
    for t in range(3000):
        top = [1, 3, 100000][t % 3]
        n = next_random() % 30 + 1
        check = (check * 31 + min_deletion(random_nums(n, top))) % 1000000007
    print(f"3000 arrays: checksum {check}")
    # the constraints' largest: 10^5 numbers of 0 and 1, then 10^5 alike
    coin = random_nums(100000, 1)
    same = [5] * 100000
    print(f"10^5 of 0 and 1 -> {min_deletion(coin)}, 10^5 alike -> {min_deletion(same)}")


main()
