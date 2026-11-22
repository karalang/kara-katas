# LeetCode #2897: Apply Operations on Array to Maximize Sum of Squares --
# the bench's Python mirror (squares.kara): the same draw, the same bit
# counts spent one at a time.


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


seed = 2897


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def main():
    count, rounds, n = 20, 20, 10000
    cases = []
    for c in range(count):
        nums = []
        for _ in range(n):
            if c % 2 == 0:
                nums.append(wide() % 1000000000 + 1)
            else:
                a = next_random() % 30
                b = next_random() % 30
                nums.append((1 << a) | (1 << b))
        k = wide() % n + 1
        cases.append((nums, k))
    total = 0
    check = 0
    for r in range(rounds):
        for nums, k in cases:
            s = max_sum(nums, k)
            total += s
            check = (check * 31 + s + r) % 1000000007
    print(f"{count} arrays of {n}, {rounds} rounds: sums total {total}, checksum {check}")


main()
