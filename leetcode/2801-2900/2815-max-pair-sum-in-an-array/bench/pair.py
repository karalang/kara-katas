# LeetCode #2815: Max Pair Sum in an Array -- the bench in Python: the ★
# arm over 20000 arrays of 100 numbers up to 10^4, all drawn first, then
# each answered 10 times.


def largest_digit(x):
    top = 0
    while x > 0:
        top = max(top, x % 10)
        x //= 10
    return top


def max_sum(nums):
    best = [0] * 10
    answer = -1
    for x in nums:
        d = largest_digit(x)
        if best[d] > 0:
            answer = max(answer, best[d] + x)
        best[d] = max(best[d], x)
    return answer


seed = 2815


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, rounds = 20000, 10
    arrays = [[next_random() % 10000 + 1 for _ in range(100)] for _ in range(count)]
    total = 0
    check = 0
    for r in range(rounds):
        for nums in arrays:
            a = max_sum(nums)
            total += a
            check = (check * 31 + a + 2 + r) % 1000000007
    print(f"{count} arrays of 100, {rounds} rounds: sums total {total}, checksum {check}")


main()
