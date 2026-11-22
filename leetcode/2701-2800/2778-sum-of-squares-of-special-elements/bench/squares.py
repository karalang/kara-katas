# LeetCode #2778: Sum of Squares of Special Elements -- the bench in
# Python: the ★ arm over 100000 random arrays, all drawn first, then each
# answered 20 times.


def sum_of_squares(nums):
    n = len(nums)
    total = 0
    for i in range(1, n + 1):
        if n % i == 0:
            total += nums[i - 1] * nums[i - 1]
    return total


seed = 2778


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count = 100000
    rounds = 20
    arrays = []
    for _ in range(count):
        n = next_random() % 50 + 1
        arrays.append([next_random() % 50 + 1 for _ in range(n)])
    total = 0
    check = 0
    for r in range(rounds):
        for nums in arrays:
            s = sum_of_squares(nums)
            total += s
            check = (check * 31 + s + r) % 1000000007
    print(f"{count} arrays, {rounds} rounds: sums total {total}, checksum {check}")


main()
