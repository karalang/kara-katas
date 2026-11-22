# LeetCode #2778: Sum of Squares of Special Elements -- the ★ arm in
# Python (squares.kara): the squares of the numbers at every 1-indexed
# place i that divides n, summed.


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
    print(sum_of_squares([1, 2, 3, 4]))
    print(sum_of_squares([2, 7, 1, 19, 18, 3]))
    print(sum_of_squares([9]))
    print(sum_of_squares([50] * 50))
    print(sum_of_squares(list(range(1, 48))))
    total = 0
    check = 0
    for _ in range(5000):
        n = next_random() % 50 + 1
        nums = [next_random() % 50 + 1 for _ in range(n)]
        s = sum_of_squares(nums)
        total += s
        check = (check * 31 + s) % 1000000007
    print(f"5000 arrays: sums total {total}, checksum {check}")


main()
