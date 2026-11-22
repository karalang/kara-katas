# LeetCode #2897: Apply Operations on Array to Maximize Sum of Squares --
# the Python mirror of the ★ arm (squares.kara): the bit counts spent one
# at a time, each of the k values taking every bit still held.


def max_sum(nums, k):
    modulus = 1000000007
    holders = [0] * 31
    for v in nums:
        for b in range(31):
            if (v >> b) & 1 == 1:
                holders[b] += 1
    total = 0
    for _ in range(k):
        value = 0
        for b in range(31):
            if holders[b] > 0:
                holders[b] -= 1
                value |= 1 << b
        total = (total + value * value) % modulus
    return total


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def main():
    global seed
    print(f"{max_sum([2, 6, 5, 8], 2)} {max_sum([4, 5, 4, 7], 3)}")
    n = 100000
    powers = [1 << (i % 30) for i in range(n)]
    print(f"{max_sum([1000000000] * n, n)} {max_sum(powers, 1)} {max_sum(powers, 30)} {max_sum(list(range(1, n + 1)), n)}")
    seed = 2897
    total = 0
    check = 0
    for c in range(3100):
        small = c < 3000
        n = next_random() % 8 + 1 if small else wide() % 99001 + 1000
        nums = []
        for _ in range(n):
            if small:
                nums.append(next_random() % 15 + 1)
            elif c % 2 == 1:
                a = next_random() % 30
                b = next_random() % 30
                nums.append((1 << a) | (1 << b))
            else:
                nums.append(wide() % 1000000000 + 1)
        k = wide() % n + 1
        best = max_sum(nums, k)
        total += best
        check = (check * 31 + best) % 1000000007
        if c == 2999:
            print(f"3000 small arrays: sums total {total}, checksum {check}")
            total = 0
            check = 0
    print(f"100 large arrays: sums total {total}, checksum {check}")


main()
